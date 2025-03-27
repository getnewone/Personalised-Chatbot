#!/bin/bash

# Install Python dependencies
pip install flask flask_sqlalchemy llama-index python-dotenv openai nltk selenium langchain-openai langchain Pillow

# Download NLTK data
python -m nltk.downloader punkt averaged_perceptron_tagger popular
python -m nltk.downloader averaged_perceptron_tagger_eng

# Create .env file and set OpenAI API key
if [ ! -f .env ]; then
  echo "Creating .env file..."
  echo "OPENAI_API_KEY=YOUR_API_KEY" > .env
  echo ".env file created. Please replace YOUR_API_KEY with your actual OpenAI API key."
else
  echo ".env file already exists."
fi

# Make the script executable
chmod +x setup.sh

echo "Setup complete! Please run the script with ./setup.sh"
