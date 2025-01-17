import os
import nltk
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from llama_index.core import StorageContext, load_index_from_storage
from langchain_community.document_loaders import SeleniumURLLoader
from dotenv import load_dotenv
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import re

# Download NLTK data
nltk.download(['punkt', 'averaged_perceptron_tagger', 'popular'])
nltk.download('averaged_perceptron_tagger_eng')

def init_index_from_url(urls, openai_api_key):
    try:
        # These steps work WITHOUT API key
        # Step 1: Web scraping
        documents = []
        for url in urls:
            loader = SeleniumURLLoader(urls=[url])
            documents.extend(loader.load())
            print("✓ URL scraping successful")

        # Step 2: Save raw text (works without API)
        input_dir = "data"
        os.makedirs(input_dir, exist_ok=True)
        data_str = '\n'.join(doc.page_content for doc in documents)
        with open(os.path.join(input_dir, "data.txt"), "w") as file:
            file.write(data_str)
        print("✓ Raw data saved")

        # These steps REQUIRE API key
        if not openai_api_key:
            print("⚠️ No API key - stopping before embedding creation")
            return None
            
        # Step 3: Create embeddings and index
        Settings.llm = OpenAI(temperature=0.7, model="gpt-3.5-turbo", max_tokens=512)
        documents = SimpleDirectoryReader(input_dir).load_data()
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        print("✓ Index created")
        
        return index

    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def save_index(index):
   index.storage_context.persist('PKL_file')


    

def load_index_from_disk():
   storage_context = StorageContext.from_defaults(persist_dir="PKL_file")
   new_index = load_index_from_storage(storage_context)
   return new_index

urls = ["https://openai.com"]
openai_api_key = os.getenv('OPENAI_API_KEY')


# Create index
index = init_index_from_url(urls, openai_api_key)

save_index(index)
# Load the index from disk
loaded_index = load_index_from_disk()

# Custom responses
custom_responses = {
    "greeting": "Hi there! This is Rick, how may I assist you today?",
    "thanks": "You're welcome! If you have any more questions, feel free to ask.",
    "farewell": "Goodbye! Have a great day!",
    "default": "I'm sorry, but I couldn't understand your question. Could you please rephrase it?",
    "chatbot-name": "This is Rick, an AI chatbot ready to help you",
    "location": '''We have multiple branches located accros the Australia. You can select as per your location: <a href= 'https://www.aghajuicetruganina.com.au/about-us'> Location <a>''',
    "book_table": "We do not book tables, but you can order from online or by phone number of specific store",
    "Review": "We got avarage 4.5 rating out of 5"
}


def remember_conversation(conversation, input_text, response):
    conversation.append((input_text, response))

# Example usage of chatbot function
query_engine = loaded_index.as_query_engine()

conversation_history = []
while True: 
    input_text = input("Question: ").lower()
  
    if input_text == "exit":
        break
    elif re.search(r'\b(hello|hi)\b', input_text):
        print(custom_responses["greeting"])
        print()
    elif 'bye' in input_text or 'goodbye' in input_text or "see you" in input_text:
        print(custom_responses["farewell"])
        print()
        remember_conversation(conversation_history, input_text, custom_responses["farewell"])
        break
    elif 'your name' in input_text or 'who are you' in input_text or 'who you are' in input_text:
        print(custom_responses["chatbot-name"])
        print()
        remember_conversation(conversation_history, input_text, custom_responses["farewell"])
    elif 'which area' in input_text or 'you located' in input_text or 'your location' in input_text:
        print(custom_responses["location"])
        print()
    elif 'table' in input_text:
        print(custom_responses["book_table"])
        print()
    elif 'Reviews' in input_text or 'Review' in input_text:
        print(custom_responses["Review"])
        print()

    
    else:
        response = query_engine.query(input_text)
        if response:
            print()
            print(f"bot: {response}")
            print()
            remember_conversation(conversation_history, input_text, response)
        else:
            print(custom_responses["default"])
            print()


#Chat with nike data

# import os
# import nltk
# from llama_index.llms.openai import OpenAI
# from llama_index.core import Settings, VectorStoreIndex
# from llama_index.core.node_parser import SentenceSplitter
# from llama_index.core import SimpleDirectoryReader
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from llama_index.core import StorageContext, load_index_from_storage
# from langchain_community.document_loaders import SeleniumURLLoader
# from dotenv import load_dotenv
# import tkinter as tk
# from tkinter import scrolledtext
# from PIL import Image, ImageTk
# import re

# # Download NLTK data
# nltk.download(['punkt', 'averaged_perceptron_tagger', 'popular'])
# nltk.download('averaged_perceptron_tagger_eng')

# def init_index_from_url(urls, openai_api_key):
#     try:
#         # These steps work WITHOUT API key
#         # Step 1: Web scraping
#         documents = []
#         for url in urls:
#             loader = SeleniumURLLoader(urls=[url])
#             documents.extend(loader.load())
#             print("✓ URL scraping successful")

#         # Step 2: Save raw text (works without API)
#         input_dir = "data"
#         os.makedirs(input_dir, exist_ok=True)
#         data_str = '\n'.join(doc.page_content for doc in documents)
#         with open(os.path.join(input_dir, "data.txt"), "w") as file:
#             file.write(data_str)
#         print("✓ Raw data saved")

#         # These steps REQUIRE API key
#         if not openai_api_key:
#             print("⚠️ No API key - stopping before embedding creation")
#             return None
            
#         # Step 3: Create embeddings and index
#         Settings.llm = OpenAI(temperature=0.7, model="gpt-3.5-turbo", max_tokens=512)
#         documents = SimpleDirectoryReader(input_dir).load_data()
#         index = VectorStoreIndex.from_documents(documents, show_progress=True)
#         print("✓ Index created")
        
#         return index

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return None


# def save_index(index):
#     index.storage_context.persist('PKL_file')

# def load_index_from_disk():
#     storage_context = StorageContext.from_defaults(persist_dir="PKL_file")
#     new_index = load_index_from_storage(storage_context)
#     return new_index

# urls = ["https://www.nike.com/au/"]
# openai_api_key = os.getenv('OPENAI_API_KEY')

# index = init_index_from_url(urls, openai_api_key)
# save_index(index)
# loaded_index = load_index_from_disk()

# custom_responses = {
#     "greeting": "Hi there! This is Rick, how may I assist you today?",
#     "thanks": "You're welcome! If you have any more questions, feel free to ask.",
#     "farewell": "Goodbye! Have a great day!",
#     "default": "I'm sorry, but I couldn't understand your question. Could you please rephrase it?",
#     "chatbot-name": "This is Rick, an AI chatbot ready to help you",
#     "location": '''We have multiple branches located across Australia. You can select as per your location: <a href= 'https://www.aghajuicetruganina.com.au/about-us'> Location <a>''',
#     "book_table": "We do not book tables, but you can order from online or by phone number of specific store",
#     "Review": "We got an average 4.5 rating out of 5"
# }

# def remember_conversation(conversation, input_text, response):
#     conversation.append((input_text, response))

# # # Initialize the UI
# import tkinter as tk
# from tkinter import scrolledtext
# from PIL import Image, ImageTk
# import re

# class ChatbotUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Chatbot")
#         self.root.geometry("600x700")

#         self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
#         self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

#         self.entry = tk.Entry(self.root)
#         self.entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10), fill=tk.X, expand=True)
#         self.entry.bind("<Return>", self.send_message)

#         self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
#         self.send_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(0, 10))

#         self.query_engine = loaded_index.as_query_engine()
#         self.conversation_history = []

#         self.initialize_chat()

#         # Load user and bot icons using PIL
#         self.user_icon = self.load_icon("icons8-person-male-skin-type-4-16.png", 30)
#         self.bot_icon = self.load_icon("icons8-chatbot-48.png", 30)

#         self.chat_area.tag_configure("user", justify="right")
#         self.chat_area.tag_configure("bot", justify="left")
#         self.chat_area.tag_configure("user_icon", justify="right")
#         self.chat_area.tag_configure("bot_icon", justify="left")

#     def load_icon(self, file_path, size):
#         image = Image.open(file_path)
#         image = image.resize((size, size), Image.LANCZOS)
#         tk_image = ImageTk.PhotoImage(image)
#         return tk_image

#     def send_message(self, event=None):
#         input_text = self.entry.get().lower()
#         self.entry.delete(0, tk.END)

#         if not input_text:
#             return

#         self.update_chat(self.user_icon, "You", input_text, "user")
#         self.root.after(900, self.generate_bot_response, input_text)

         
#     def generate_bot_response(self, input_text):
#         if input_text == "exit":
#             self.root.quit()
#         elif re.search(r'\b(hello|hi)\b', input_text):
#             response = custom_responses["greeting"]
#         elif 'bye' in input_text or 'goodbye' in input_text or "see you" in input_text:
#             response = custom_responses["farewell"]
#         elif 'your name' in input_text or 'who are you' in input_text or 'who you are' in input_text:
#             response = custom_responses["chatbot-name"]
#         elif 'which area' in input_text or 'you located' in input_text or 'your location' in input_text:
#             response = custom_responses["location"]
#         elif 'table' in input_text:
#             response = custom_responses["book_table"]
#         elif 'reviews' in input_text or 'review' in input_text:
#             response = custom_responses["Review"]
#         else:
#             response = self.query_engine.query(input_text)
#             response = response if response else custom_responses["default"]
        
        
#         self.update_chat(self.bot_icon, "Bot", response, "bot")
#         remember_conversation(self.conversation_history, input_text, response)

        

#     def update_chat(self, icon, sender, message, tag):
#         self.chat_area.config(state='normal')
#         if tag == "user":
#             self.chat_area.insert(tk.END, f"{sender}: {message}\n", "user")
#             self.chat_area.image_create(tk.END, image=icon)
#             self.chat_area.insert(tk.END, "\n", "user")
#         else:
#             self.chat_area.image_create(tk.END, image=icon)
#             self.chat_area.insert(tk.END, f" {sender}: {message}\n", "bot")
#         self.chat_area.config(state='disabled')
#         self.chat_area.yview(tk.END)

#     def initialize_chat(self):
#         # Initialize chat messages if needed
#         self.bot_icon = self.load_icon("icons8-chatbot-48.png", 30)
#         self.update_chat(self.bot_icon, "Bot", "Hello! Welcome to the chatbot interface.", "bot")
#         self.update_chat(self.bot_icon, "Bot", "Feel free to start a conversation.", "bot")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ChatbotUI(root)
#     root.mainloop()
