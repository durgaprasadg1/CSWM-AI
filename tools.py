from datetime import datetime
from utilities.utilities import log
import requests
import json

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url = f"https://wttr.in/{city}/?format=3"

    response = requests.get(url, timeout=10)

    response.raise_for_status() #Agr kuch fat ta hai error aata hai to yha hit hoga aur agent loop me catch (except) me fasega. else response jaega
        
    return response.text
    

def get_current_city():
    return "Gondia"

tools=[
    {
        "type":"function",
        "function":{
            "name": "get_current_time",
            "description": "Returns the current date and time in formatted string.",
            "parameters":{"type" : "object", "properties":{}}
        }
    },

    {
        "type":"function",
        "function":{
            "name": "get_city_weather",
            "description": "Returns the current whether of given city in formatted string.",
            "parameters": {
                "type" : "object", 
                "properties":{
                    "city":{
                        "type": "string",
                        "description": "city to get weather for"
                    }
                },
                "required" : ["city"]
            }
        }
    },
    {
        "type" : "function",
        "function":{
            "name": "get_current_city",
            "description": "Returns the current city of user, useful when he use terms like my city, my location, current city, where I live, etc.",
            "parameters": {"type" : "object",  "properties":{}}
        }
    }
]


FUNCTION_NAME_TO_FUNCTION_IMPLE_MAP = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
    "get_current_city": get_current_city
}




#  {
#         "type":"function",
#         "function":{
#             "name": "get_current_time",
#             "description": "Returns the current date and time in formatted string.",
#             "parameters":{
#                 "type":"object",
#                 "properties":{
#                     "city":{
#                         "type": "string",
#                         "description": "Name of the city"    
#                     },
#                     "country":{
#                         "type":"string",
#                         "description": "Name of country in which that city is located",
#                     }
#                 },
#                 "required" : ["city"]
#             } 
#         }
#     }

# Aisa hota hai ek ek tool + params


def runTool(tool_call):
    func_name = tool_call.function.name
    func_args = {}

    try:
        func_args = json.loads(tool_call.function.arguments or "{}")

        log(f" 🪛 Executing tool '{func_name}' with arguments: {func_args}")

        fn = FUNCTION_NAME_TO_FUNCTION_IMPLE_MAP[func_name]
        result = fn(**func_args)


    except Exception as e:
        result = f"Error occurred while executing the tool '{func_name}': {str(e)}"

    log(f" ➡️ { result}")
    return result