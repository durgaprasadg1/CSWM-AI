# std libs
import os

#3rd party libs
from openai import OpenAI
from dotenv import load_dotenv

#local libs
from tools import tools, runTool
from utilities.utilities import log
from types import SimpleNamespace


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



def stream_chat(messages):
    stream = client.chat.completions.create(
        model=os.getenv('MODEL'),
        messages=messages,
        tools=tools,
        stream=True,
    )

    full_response = ""
    calls= {}
    is_assistant_label_printed = False


    # streaiming response from LLM, printing it as it comes in, and also collecting tool calls if any 
    try:
        for chunk in stream :

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            #do we have content to print ?
            if delta.content:
                if not is_assistant_label_printed:
                    print("Assistant: ", end="", flush=True)
                    is_assistant_label_printed = True

                print(delta.content, end="", flush=True)
                full_response += delta.content



            #if we have tool calls from LLM, 
            if(delta.tool_calls and len(delta.tool_calls) > 0):
                calls = delta.tool_calls

                for tool_call in calls:

                    # getOrDefault hai java jaise

                    obj = calls.setdefault(tool_call.index, SimpleNamespace(
                        id=None, function=SimpleNamespace(name=None, arguments=None)
                    ))

                    # Vo object aa gya abb usme tool call ki info append karna hai 

                    if tool_call.id:
                        obj.id = tool_call.id

                    if tool_call.function and tool_call.function.name:
                        obj.function.name = tool_call.function.name


                    if tool_call.function and tool_call.function.arguments:
                        obj.function.arguments = tool_call.function.arguments

    except KeyboardInterrupt:
        print("Response Stopped by user.")
        calls ={}

        


    if is_assistant_label_printed:
        print("", flush=True)

    call_list =[]

    for key in sorted(calls):
        call_list.append(calls[key])
    return full_response,call_list 




def build_tool_calls_payload(tool_calls):
    """
    Build a list of tool calls payloads from the tool_calls list.
    """

    payload = []
    for tool_call in tool_calls:
        tool_call_dict = {
            "id": tool_call.id,
            "type": "function",
            "function":{
                "name": tool_call.function.name,
                "arguments": tool_call.arguments,
            },

        }
        payload.append(tool_call_dict)

    return payload

    
while True:

    print("Type 'exit', 'quit', or 'bye' to end the chat.")
    try:

        client_query= input("User : ")
    except KeyboardInterrupt:
        print("\nExiting the chat...")
        break
    
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

        full_response, tool_calls = stream_chat(messages)
        
        # msg = response.choices[0].message
        log(f"{steps+1} model requested {len(tool_calls)} tool calls.")

        if not tool_calls:
            break

        messages.append({
            "role":"assistant",
            "content" : full_response,
            "tool_calls" : build_tool_calls_payload(tool_calls)
        })

        for tool_call in tool_calls:
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

        
  
