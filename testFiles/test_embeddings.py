from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv() # import env vars

client  = OpenAI(
    base_url = os.getenv('BASE_URL') , #ollama running hai iss jagah pe 
    api_key = os.getenv('API_KEY')
)



response = client.embeddings.create(
    model=os.getenv("EMBED_MODEL"),
    # input="I am a good boy"
    input=["I am a good boy", "I love you"]
)


print("generating response : " ,response.data[0].embedding)
# print("--------------------------------------------")
# print(response.data[1].embedding)