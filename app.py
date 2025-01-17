from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import os
import re
from llama_index.core import StorageContext, load_index_from_storage
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

app = Flask(__name__, static_url_path='/static')

# Load the index from disk
def load_index_from_disk():
   storage_context = StorageContext.from_defaults(persist_dir="PKL_file")
   new_index = load_index_from_storage(storage_context)
   return new_index

# Initialize loaded_index outside of the Flask app
loaded_index = load_index_from_disk()

# Route to handle bot requests
chat_history = []

@app.route('/Static/<path:filename>')
def serve_static(filename):
    return send_from_directory('Static', filename)

@app.route('/Pikatro/bot', methods=['GET', 'POST'], )
def pikatro_bot():
    try:
        if request.method == 'POST':
            user_input = request.form.get('user_input')
            
            # Input validation
            if not user_input:
                return custom_responses["empty_input"], 400
            if len(user_input) > 500:
                return custom_responses["too_long"], 400
                
            try:
                response = process_user_input(user_input)
                chat_history.append({'user': user_input, 'bot': str(response)})
                return str(response)
            except Exception as e:
                app.logger.error(f"Error processing input: {str(e)}")
                return custom_responses["api_error"], 500
                
        return render_template('bot_template.html', chat_history=chat_history)
        
    except Exception as e:
        app.logger.error(f"Server error: {str(e)}")
        return custom_responses["error"], 500

# Custom responses
custom_responses = {
    # Greetings
    "greeting": "Hi there! This is Rick, how may I assist you today?",
    "greeting_time": {
        "morning": "Good morning! How can I help you today?",
        "afternoon": "Good afternoon! What can I do for you?",
        "evening": "Good evening! How may I assist you?",
        "night": "Hello! Having a late night? How can I help?"
    },
    
    # Farewells
    "farewell": "Goodbye! Have a great day!",
    "farewell_alt": "Take care! Feel free to come back if you need anything.",
    "goodbye_night": "Good night! Sleep well!",
    
    # Identity/Introduction
    "chatbot-name": "This is Rick, an AI chatbot ready to help you",
    "purpose": "I'm here to assist you with information and answer your questions!",
    "capabilities": "I can help you with information, answer questions, and guide you through our services.",
    
    # Pleasantries
    "how_are_you": "I'm functioning well, thank you for asking! How can I assist you?",
    "Nice": "Nice to meet you too, how may I help you?",
    "thanks": "You're welcome! If you have any more questions, feel free to ask.",
    "welcome": "You're welcome! Is there anything else you'd like to know?",
    
    # Status/Condition
    "doing_well": "That's great to hear! How can I assist you today?",
    "doing_bad": "I'm sorry to hear that. Is there anything I can help you with?",
    
    # Acknowledgments
    "understand": "I understand. Please go ahead with your question.",
    "processing": "Let me think about that for a moment...",
    "clarification": "Could you please provide more details about that?",
    
    # Error Handling
    "error": "I apologize, but I'm having trouble processing your request right now. Please try again.",
    "api_error": "I'm currently experiencing some technical difficulties. Please try again in a moment.",
    "invalid_input": "I couldn't understand that input. Could you please rephrase it?",
    "too_long": "Your message is too long. Please try a shorter message.",
    "empty_input": "Please type a message before sending.",
    "rate_limit": "I'm receiving too many messages. Please wait a moment before trying again.",
    "default": "I'm sorry, but I couldn't understand your question. Could you please rephrase it?",
    
    # Small Talk
    "weather": "I don't actually experience weather, but I'd be happy to help you with something else!",
    "joke": "I'm better at helping with questions than telling jokes, but I'll try my best to assist you!",
    "age": "I'm an AI assistant, so I don't have an age. How can I help you today?",
    "meaning_of_life": "That's a deep question! I'm better at helping with more practical matters. What can I assist you with?",
    
    # Business Related
    "contact": "You can contact our staff through our website or call us at [phone number]",
    "hours": "We're open Monday to Friday 9 AM to 6 PM, and weekends 10 AM to 4 PM",
    "location": "We're located at [your address]. Would you like directions?",
    
    # Feedback
    "positive_feedback": "Thank you for the kind words! I'm glad I could help.",
    "negative_feedback": "I apologize for not meeting your expectations. I'll try to do better.",
    
    # Emergency
    "emergency": "If this is an emergency, please contact emergency services directly at 911."
}

query_engine = loaded_index.as_query_engine()
# Function to process user input and generate bot response
def process_user_input(user_input):
    time.sleep(1)
    input_lower = user_input.lower()
    
    # Greetings
    if re.search(r'\b(hello|hi|hey|howdy|hola)\b', input_lower):
        return custom_responses["greeting"]
    elif re.search(r'\b(good morning)\b', input_lower):
        return custom_responses["greeting_time"]["morning"]
    elif re.search(r'\b(good afternoon)\b', input_lower):
        return custom_responses["greeting_time"]["afternoon"]
    elif re.search(r'\b(good evening)\b', input_lower):
        return custom_responses["greeting_time"]["evening"]
    elif re.search(r'\b(good night)\b', input_lower):
        return custom_responses["greeting_time"]["night"]
    
    # Farewells
    elif any(keyword in input_lower for keyword in ['bye', 'goodbye', 'see you', 'cya', 'farewell']):
        return custom_responses["farewell"]
    elif 'good night' in input_lower:
        return custom_responses["goodbye_night"]
    
    # Identity Questions
    elif any(keyword in input_lower for keyword in ['your name', 'who are you', 'who you are', 'what are you']):
        return custom_responses["chatbot-name"]
    
    # Pleasantries
    elif re.search(r'\b(how are you|how\'re you|how do you do)\b', input_lower):
        return custom_responses["how_are_you"]
    elif 'nice to meet' in input_lower:
        return custom_responses["Nice"]
    elif any(keyword in input_lower for keyword in ['thanks', 'thank you', 'thankyou', 'thx']):
        return custom_responses["thanks"]
    
    # Location Related
    elif any(keyword in input_lower for keyword in ['where', 'located', 'location', 'address', 'place']):
        return custom_responses["location"]
    
    # Feedback
    elif any(keyword in input_lower for keyword in ['great job', 'well done', 'awesome', 'excellent']):
        return custom_responses["positive_feedback"]
    elif any(keyword in input_lower for keyword in ['bad job', 'terrible', 'worst', 'useless']):
        return custom_responses["negative_feedback"]
    
    # Emergency
    elif any(keyword in input_lower for keyword in ['emergency', 'urgent', 'help me', '911']):
        return custom_responses["emergency"]
    
    # Default Response
    else:
        response = query_engine.query(user_input)
        if response:
            return response
        else:
            return custom_responses["default"]

if __name__ == '__main__':
    app.run(debug=True, port=2023)

#UI with tkinter

# import customtkinter as ctk
# import requests

# class ChatbotUI(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("Rick's Chatbot")
#         self.geometry("400x600")

#         # Create chat log text box
#         self.chat_log = ctk.CTkTextbox(self, width=350, height=400)
#         self.chat_log.pack(pady=20)

#         # Create input field
#         self.input_field = ctk.CTkEntry(self, width=300)
#         self.input_field.pack(pady=10)

#         # Create send button
#         self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message)
#         self.send_button.pack(pady=10)

#         # Initialize conversation history
#         self.conversation_history = []

#     def send_message(self):
#         input_text = self.input_field.get()
#         self.input_field.delete(0, ctk.END)

#         # Send post request to chatbot
#         response = requests.post("http://localhost:5000/chatbot", json={"input_text": input_text})

#         # Display response
#         response_text = response.json()["response"]
#         self.chat_log.insert(ctk.END, f"User: {input_text}\n")
#         self.chat_log.insert(ctk.END, f"Bot: {response_text}\n\n")
#         self.conversation_history.append((input_text, response_text))

#     def run(self):
#         self.mainloop()

# if __name__ == "__main__":
#     app = ChatbotUI()
#     app.run()



