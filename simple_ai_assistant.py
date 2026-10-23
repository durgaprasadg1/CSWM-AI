from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv() # import env vars
client = OpenAI(
    base_url = os.getenv('BASE_URL') , #ollama running hai iss jagah pe 
    api_key = os.getenv('API_KEY')
)
messages = []

messages.append(
    {
        "role":"system",
        "content": "Act as the technical person, who responds in 100 words."
    }
)
while True:

    print("Type 'exit', 'quit', or 'bye' to end the chat.")
    client_query= input("User : ")

    if client_query.lower() in ["exit", "quit", "bye"]:
        print("Exiting the chat...")
        break


    # added query
    messages.append(
            {
                "role": "user", 
                "content":client_query 
            }
        )
    response = client.chat.completions.create(
        model=os.getenv('MODEL'),
        messages=messages
    )
    res = response.choices[0].message.content

    # added reply
    messages.append(
                {
                    "role": "assistant", 
                    "content": res
                }
            )

    print("Assistant :", res)