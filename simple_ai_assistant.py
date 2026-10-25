# std libs
import os

#3rd party libs
from openai import OpenAI
from dotenv import load_dotenv

#local libs
from tools import tools, runTool
from utilities.utilities import log


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
        "content": "You are the one who responds to Science, Technology, Engineering, and Mathematics (STEM) related queries. response must be in 100 words and also give suggestions for further reading to user."
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
        log(f"{steps+1} model requested {len(msg.tool_calls)} tool calls.")

        if not msg.tool_calls:
            break

        messages.append(msg)

        for tool_call in msg.tool_calls:
            result = runTool(tool_call)

            messages.append({
                "role":"tool", 
                "tool_id" : tool_call.id,
                "content": str(result),
            })

    
    else: # else after for loop, executed when break is not called, i.e. max steps reached

        fallback_msg = "Sorry, I could not finish task within step limit."
        messages.append({
            "role":"assistant",
            "content": fallback_msg
        })
        print("Assistant: ", fallback_msg)
        continue

        
    messages.append({
        "role":"assistant",
        "content":msg.content
    })

    print("Assistant: ", msg.content or "")
