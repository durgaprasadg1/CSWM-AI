from datetime import datetime

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")




tools=[
    {
        "type":"function",
        "function":{
            "name": "get_current_time",
            "description": "Returns the current date and time in formatted string.",
            "parameters":{"type" : "object", "properties":{}}
        }
    }
]


FUNCTION_NAME_TO_FUNCTION_IMPLE_MAP = {
    "get_current_time": get_current_time,
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