from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Can you help me to choose which card design is looks more batter, good, stylish?"},
        {
          "type": "image_url",
          "image_url": {
            "url": "Images/Screenshot 2024-06-11 at 9.21.36 AM.png",
          },
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "Images/Screenshot 2024-06-11 at 9.22.25 AM.png",
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0])