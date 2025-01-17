from llama_index.llms.openai import OpenAI
import os
import re
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex,  ServiceContext, PromptHelper
from langchain_openai import OpenAI
from llama_index.core.llms import LLM
from llama_index.core import StorageContext, load_index_from_storage
from langchain_community.document_loaders import SeleniumURLLoader

# Set OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define custom responses
custom_responses = {
    "greeting": "Hi there! This is Rick, how may I assist you today?",
    "thanks": "You're welcome! If you have any more questions, feel free to ask.",
    "farewell": "Goodbye! Have a great day!",
    "default": "I'm sorry, but I couldn't understand your question. Could you please rephrase it?",
    "chatbot-name": "This is Rick, an AI chatbot ready to help you",
    
}

def remember_conversation(conversation, input_text, response):
    conversation.append((input_text, response))

def assess_personality():
    questions = [
        "What are your main interests or hobbies?",
        "What do you consider your strengths?",
        "What areas do you think you need improvement in?",
        "Do you prefer working alone or in a team?",
        "What kind of challenges do you enjoy?",
        "How do you handle stress or pressure?",
        "What motivates you?",
        "Do you enjoy taking risks or do you prefer a more cautious approach?"
    ]

    answers = []
    for question in questions:
        answer = input(question + " ")
        answers.append(answer)

    # Analyze answers based on text data
    personality_traits = []
    with open("data/document.txt", "r") as file:
        text_data = file.read()
        for answer in answers:
            if answer.lower() in text_data.lower():
                personality_traits.append(answer)

    # Provide response or judgment based on personality traits
    if personality_traits:
        print("Based on your answers and our analysis, we can say you are:")
        for trait in personality_traits:
            print(f"- {trait}")
    else:
        print("Sorry, we couldn't determine your personality based on the provided answers.")

# Initialize index from URL
def init_index_from_url(urls, openai_api_key):
    # Model parameters
    max_input_size = 4096
    num_outputs = 512

    # LLM predictor with LangChain ChatOpenAI
    prompt_helper = PromptHelper(max_input_size, num_outputs, chunk_overlap_ratio=0.2, chunk_size_limit=600)
    llm_predictor = OpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs)
   
    # Load text data from URL
    documents = []
    for url in urls:
        loader = SeleniumURLLoader(urls=[url])
        documents.extend(loader.load())

    input_dir = "data"
    os.makedirs(input_dir, exist_ok=True)
    data_str = '\n'.join(doc.page_content for doc in documents)
    with open(os.path.join(input_dir, "document.txt"), "w") as file:
        file.write(data_str)

    # Init index with text data
    documents = SimpleDirectoryReader(input_dir).load_data()
    service_context = ServiceContext.from_defaults(prompt_helper=prompt_helper, llm_predictor=llm_predictor)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True)

    return index

# Save index to disk
def save_index(index):
   index.storage_context.persist('PKL_file')

# Load index from disk
def load_index_from_disk():
   storage_context = StorageContext.from_defaults(persist_dir="PKL_file")
   new_index = load_index_from_storage(storage_context)
   return new_index

urls = ["https://openai.com"]
openai_api_key = os.getenv("OPENAI_API_KEY")

# Create index
index = init_index_from_url(urls, openai_api_key)
save_index(index)

# Load the index from disk
loaded_index = load_index_from_disk()
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
    elif "check my personality" in input_text:
        assess_personality()
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
