import json
import importlib
import google.generativeai as genai
# from google.generativeai import content_types
from collections.abc import Iterable
import os
from functions import functions
from functions import get_current_weather

genai.configure(api_key=os.environ['API_KEY'])
API_KEY = 'AIzaSyDWTBDS_qfcf_enGpDJ5xHQRmwqkcfFW28'

# Dynamically import functions from the 'functions' module
def get_functions():    
    functions_module = importlib.import_module('functions')
    available_functions = {
        name: getattr(functions_module, name) 
        for name in dir(functions_module) 
        if callable(getattr(functions_module, name)) and not name.startswith('_')
    }
    return available_functions

def function_calling_agent():
    """
    A function-calling agent that interacts with the user through the terminal and uses the Gemini model.
    """    
    # Get the available functions
    available_functions = get_functions()
    #print("Available functions: ", available_functions)

    print("Function Calling Agent (powered by Gemini) is ready!")
    print("Available functions:")
    functions = []
    for func_name in available_functions:
      functions.append(available_functions[func_name])
      print(f"- {func_name}") #, type(available_functions[func_name]))
        
    instruction = """You are a function calling agent. You are able to look at all the functions and call the correct one based on the user's input. 
                    If you are not given enough parameters, you should ask for the missing parameters. Do not perform any other tasks."""

    model = genai.GenerativeModel(
        "models/gemini-1.5-pro", tools=functions, system_instruction=instruction

    )
    
    # Start the chat
    chat = model.start_chat(enable_automatic_function_calling=True, history = [])
    msgs = []
    
    while True:
        user_input = input("Enter a command or 'exit' to quit: ")        
            
        if user_input.lower() == 'exit':
            break

        try:
            # tool_config = tool_config_from_mode("auto")
            response = chat.send_message(user_input)
            print("Chat History: ", chat.history)
            if response.candidates[0].content is not None:
                text = response.candidates[0].content.parts[0].text
                print("Output: ", text)                
                if isinstance(text, dict):
                    print(json.dumps(text, indent=2))
                else:
                    print(text)

            else:
                print(response.text)

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    function_calling_agent()