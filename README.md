# AI Brochure Generator using Gradio

This is a beginner-friendly Python project that generates brochure-style content using the OpenAI API and provides an interactive web interface using Gradio.

---

## What This Project Does

- Takes website content as input
- Uses AI to generate brochure-style text
- Provides a simple Gradio interface for interaction
- Reads the API key securely from a `.env` file
- Can also be explored in a Jupyter Notebook

---

## Tools Used

- Python
- OpenAI
- Gradio
- Jupyter Notebook
- python-dotenv

---

## Files in This Project

- `app.py` — main application file with the Gradio interface
- `brochure_gardio.ipynb` — notebook version of the project
- `README.md` — project documentation
- `pyproject.toml` — project configuration and dependencies
- `uv.lock` — dependency lock file
- `.gitignore` — prevents unnecessary or secret files from being uploaded
- `.python-version` — Python version configuration

---

## How to Set Up

1. Open the project folder in VS Code.
2. Install the required dependencies.
3. Create a `.env` file in the project folder.
4. Add your OpenAI API key inside the `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## How to Run

Run the application using:

```bash
python app.py
```

After running the file, Gradio will generate a local link in the terminal.

Open that link in your browser to use the app.

---

## Features

- AI-generated brochure content
- Simple and interactive Gradio UI
- Secure API key handling
- Beginner-friendly structure
- Notebook support for experimentation

---

## Important Note

Do not upload your `.env` file to GitHub because it contains your private API key.

---

## What I Learned

This project helped me learn:

- How to use the OpenAI API
- How to build AI-powered Python applications
- How to create a Gradio web interface
- How to securely manage API keys
- How to structure a small Python project
- How to work with Jupyter Notebooks
