from datetime import datetime
import requests


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url = f"https://wttr.in/{city}/?format=3"

    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.text
    else :
        return f"Could not retrieve weather information for {city}. Please try again later."

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
    }
]


FUNCTION_NAME_TO_FUNCTION_IMPLE_MAP = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
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