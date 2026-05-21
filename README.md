AI Brochure Generator
This is a beginner-friendly Python project that creates brochure-style text using the OpenAI API and provides an interactive web interface with Gradio. Gradio is an open-source Python package for quickly building web apps and demos around Python functions, and its Interface class lets developers wrap a Python function with input and output components in just a few lines.

What this project does
Gets content from a website.

Uses AI to turn that content into brochure-style text.

Reads the API key from a .env file.

Can be run in a Python script or a Jupyter notebook.

Includes a Gradio interface so users can interact with the brochure generator in the browser, which aligns with Gradio's design for building shareable browser-based demos for Python workflows.

Tools used
Python

OpenAI

requests

BeautifulSoup

python-dotenv

Jupyter Notebook

Gradio

Files in this project
main.py — main Python file.

build_brochure.py — Python version of the project.

build_brochure.ipynb — notebook version of the project.

pyproject.toml — project setup file.

uv.lock — dependency lock file.

.env — file for your API key.

.gitignore — file that keeps secret files out of GitHub.

How to set up
Open the project folder in VS Code.

Make sure the required packages are installed.

Create a .env file in the project folder.

Add your API key inside the .env file like this:

text
OPENAI_API_KEY=your_api_key_here
How to run
Run the Python file
bash
python main.py
Run the notebook
Open:

bash
build_brochure.ipynb
Run the Gradio app
If your Gradio interface is inside the Python file, run the script and Gradio will launch a local browser-based app, typically on a local address, using launch().

bash
python main.py
Important note
Do not upload your .env file to GitHub because it contains your private API key.

What I learned
This project helped me learn:

How to use APIs.

How to keep API keys safe.

How to work with web scraping.

How to use AI in Python.

How to build a small Python project.

How to create a simple browser-based interface with Gradio for a Python application, using input and output components around a Python function.
