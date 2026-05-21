import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from IPython.display import display, Markdown, update_display
from openai import OpenAI
import gradio as gr
import json
import time

# Setting up the APIs
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

if openai_api_key:
    print(f'API key found and begins with {openai_api_key[:5]}')
else:
    print('No API key was found')
if anthropic_api_key:
    print(f'API key found and begins with {anthropic_api_key[:5]}')
else: 
    print('No API key was found')

# Creating Python Client library
openai = OpenAI()

anthropic_url = "https://api.anthropic.com/v1/"

anthropic = OpenAI(base_url=anthropic_url, api_key=anthropic_api_key)

# Creating a Class for Website-Scraping
class WebsiteScraper:
    def __init__(self, headers=None):
        default_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
        # Uses custom headers if provided
        self.headers = headers if headers else default_headers

    def get_soup(self, url):
            """
            Sending request and return BeautifulSoup object
            """
            response = requests.get(url, headers=self.headers)

            return BeautifulSoup(response.content, "html.parser")
        
    def fetch_website_contents(self, url):
            """
            Fetching the contents of the website
            """
            soup = self.get_soup(url)
            title = soup.title.string if soup.title else "No title found"

            text = ""
            if soup.body:
                for tag in soup(['script', 'style', 'img', 'input']):
                    tag.decompose()

                text = soup.body.get_text(separator= '\n', strip=True)

            return (title + text)[:2_000]
        
    def fetch_links(self, url):
            """
            Fetching all the links on a webpage 
            """

            soup = self.get_soup(url)

            links = []

            for link in soup.find_all('a'):
                href = link.get('href')

                if href:
                    links.append(href)

            return links
    
links_system_prompt = """
You are a helpdul assistant. You are tasked with analyzing all the links of a website at a given url
and find out or decide which of these links could be relative to the website to create a brochure about the
company.
Some examples of important links are to an about page, a company page, and/or to jobs/careers page. 
Important note:- The abovementioned links are just an examply, there could be more important and relative links,
so select accordingly.
You should respond in full https URL in JSON object as follows:

{
    'links': [
        {'type':'about page, 'url': "https://full.url/goes/here/about"},
        {'type':'company page', 'url': "https://another.full.url/careers"}
    ]
}

"""

# Craeting an Object
scraper = WebsiteScraper()

def get_links_user_prompt(url):
    user_prompt= """
You are provided with a list of links to a company's website.
Select the relative webpages which will be used to create a company brochure.
Do not include links such as terms of services, privacy and email links.

Links(Some might be useful):


"""
    links = scraper.fetch_links(url)
    user_prompt += '\n'.join(links)
    return user_prompt

def select_relevant_links(url):
    print(f'Selecting relevant links for this website {url}')

    response = openai.chat.completions.create(
        model= 'gpt-5-mini',
        messages= [
            {'role':'system', 'content':links_system_prompt},
            {'role':'user', 'content': get_links_user_prompt(url)}
        ]
    )
    result = response.choices[0].message.content
    links = json.loads(result)
    print(f"Found {len(links['links'])} relevant links")
    return links

# Summing up the informationto give to the LLM
def fetch_page_and_links(url):
    content = scraper.fetch_website_contents(url)
    relevant_links = select_relevant_links(url)

    result = f"## Landing Page!: \n\n{content}\n Relevant Links:\n"
    for link in relevant_links['links']:
        result += f"\n\n## Link Type: {link['type']}\n"
        result += scraper.fetch_website_contents(link['url'])

        time.sleep(2)

    return result

brochure_system_prompt = """
You are a helpful assistant and you will analyze the contents of a company's website
and all of it's relative webpages at a given url and build a short brochure about the company.
You are to decide which of the things you would like to include in the brochure, things such as
company's culture, customers and jobs/careers, if you have the information.
Respond in Markdown using headings and all that without codeblocks.
"""

def get_user_brochure_prompt(company_name, url):
    user_prompt = f"You are looking at a company called {company_name}:\
    Here are the contents of its landing page and all of its\
    relevant links and pages. Use this informartion to build a\
    short brochure about the company.\
    I repeat Respond in Markdown style without codeblocks.\n\n"
    
    user_prompt += fetch_page_and_links(url)
    return user_prompt[:5_000]

def build_brochure_gpt(company_name, url):
    messages = [
        {'role':'system', 'content':brochure_system_prompt},
        {'role':'user', 'content':get_user_brochure_prompt(company_name, url)}
    ]
    stream = openai.chat.completions.create(
        model='gpt-5-mini',
        messages= messages,
        stream=True
    )
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
        yield response

def build_brochure_claude(company_name, url):
    messages = [
        {'role':'system', 'content':brochure_system_prompt},
        {'role':'user', 'content':get_user_brochure_prompt(company_name, url)}
    ]
    stream = anthropic.chat.completions.create(
        model='claude-sonnet-4-5-20250929',
        messages= messages,
        stream=True
    )
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
        yield response

def stream_brochure_llm(company_name, url, model):
    yield ""
    if model == 'GPT':
        result = build_brochure_gpt(company_name, url)
    elif model == 'CLAUDE':
        result = build_brochure_claude(company_name, url)
    else:
        raise  ValueError('No such model exists!')
    
    yield from result

name_input = gr.Textbox(label="Enter a company name")
url_input = gr.Textbox(label="Landing page URL including http:// or https://")
model_selector = gr.Dropdown(['GPT', 'CLAUDE'], label='SELECT MODEL', value='GPT')
message_output = gr.Markdown(label='Response:')

view = gr.Interface(
    fn=stream_brochure_llm,
    inputs=[name_input, url_input, model_selector],
    outputs=[message_output],
    examples=[['Hugging Face', 'https://huggingface.co', 'GPT'], ['Ed Donner', 'https://edwarddonner.com', 'CLAUDE']],
    flagging_mode='never'
)
view.launch()