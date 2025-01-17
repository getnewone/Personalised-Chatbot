
import openai
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
openai.api_key = os.getenv('OPENAI_API_KEY')

response = openai.images.generate(
  model="dall-e-3",
  prompt=input("describe your image: "),
  size="1024x1792",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print("Image: ", image_url)


   
   

