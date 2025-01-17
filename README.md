# Personalised Chatbot Using RAG

This Chatbot is an AI-powered chatbot that can assist users with various queries. It uses OpenAI's GPT-3.5-turbo model for generating responses and integrates with a web interface built using Flask and a desktop interface using Tkinter.

## Features
- Web scraping using Selenium
- Text processing with NLTK
- Embedding creation with OpenAI
- Web interface with Flask
- Desktop interface with Tkinter

## Prerequisites
- Python 3.10 or higher
- pip (Python package installer)
- Chrome browser (for Selenium)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/ricks-chatbot.git
    cd ricks-chatbot
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv botenv
    source botenv/bin/activate  # On Windows use `botenv\Scripts\activate`
    ```

3. **Install required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    - Create a [`.env`](.env ) file in the root directory and add your OpenAI API key:
    ```plaintext
    OPENAI_API_KEY=your-actual-openai-api-key
    ```

5. **Download NLTK data:**
    ```bash
    python -m nltk.downloader punkt averaged_perceptron_tagger popular averaged_perceptron_tagger_eng
    ```

## Running the Chatbot

### Step 1: Scrape Data and Create Embeddings

1. **Run the [bot_web.py](http://_vscodecontentref_/1) script to scrape data and create embeddings:**
    ```bash
    python bot_web.py
    ```

    This script will:
    - Scrape data from specified URLs
    - Store the scraped data in [data.txt](http://_vscodecontentref_/2)
    - Create embeddings and save them in [PKL_file](http://_vscodecontentref_/3)

### Step 2: Start the Flask Server

1. **Start the Flask server:**
    ```bash
    python app.py
    ```

2. **Open your browser and navigate to:**
    ```
    http://localhost:2023
    ```

### Step 3: Interact with the Chatbot

1. **Use the web interface to interact with the chatbot.**


## Troubleshooting

1. **NLTK Data Not Found:**
    - Ensure you have downloaded the required NLTK data:
    ```bash
    python -m nltk.downloader punkt averaged_perceptron_tagger popular averaged_perceptron_tagger_eng
    ```

2. **Invalid OpenAI API Key:**
    - Make sure your [`.env`](.env ) file contains a valid OpenAI API key.

3. **Selenium WebDriver Issues:**
    - Ensure you have Chrome installed and the correct version of ChromeDriver.

