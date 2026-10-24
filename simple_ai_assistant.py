from openai import OpenAI
from dotenv import load_dotenv
from tools import tools, FUNCTION_NAME_TO_FUNCTION_IMPLE_MAP
import json
import os


load_dotenv() # import env vars
client = OpenAI(
    base_url = os.getenv('BASE_URL') , #ollama running hai iss jagah pe 
    api_key = os.getenv('API_KEY')
)
messages = []
MAX_STEPS=5  # safety limit for tool calling, to avoid infinite loops in case of bugs in the model or tools

messages.append(
    {
        "role":"system",
        "content": "Act as the technical person, who responds in 10 words."
    }
)
while True:

    print("Type 'exit', 'quit', or 'bye' to end the chat.")
    client_query= input("User : ")

    if client_query.lower() in ["exit", "quit", "bye"]:
        print("Exiting the chat...")
        break


    # added query
    messages.append({
                "role": "user", 
                "content":client_query 
                
            }
        )
    
    #chained tool calling
    for steps in range(MAX_STEPS):

        response = client.chat.completions.create(
                model=os.getenv("MODEL"),
                messages=messages,
                tools=tools,
            )
        
        
        msg = response.choices[0].message

        if not msg.tool_calls:
            break

        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = {}

            try:
                func_args = json.loads(tool_call.function.arguments or "{}")
                fn = FUNCTION_NAME_TO_FUNCTION_IMPLE_MAP[func_name]
                result = fn(**func_args)
                
            except Exception as e:
                result = f"Error occurred while executing the tool '{func_name}': {str(e)}"

            messages.append({
                "role":"tool", 
                "tool_id" : tool_call.id,
                "content": str(result),
            })

    

    messages.append({
        "role":"assistant",
        "content":msg.content
    })

    print("Assistant: ", msg.content)
