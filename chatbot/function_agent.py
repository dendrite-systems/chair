import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

def get_current_weather(location: str) -> str:
    """Gets the current weather for a given location."""
    # In a real implementation, you'd call an external weather API here.
    # For this example, we'll return a mock response.
    return f"The weather in {location} is currently sunny and 75 degrees Fahrenheit."

# Define available functions
available_functions = {
    "get_current_weather": get_current_weather,
}

# Generate a response with function calling
response = genai.generate_text(
    model="gemini-1.5-flash",
    prompt="What's the weather like in San Francisco?",
#     tool_code=f"""
# # This request needs following APIs from available ones: get_current_weather
# # I already know API descriptions for all of them.
# get_current_weather(location="San Francisco")
#     """,
)

# If the model decides to call a function, execute it
if response.candidates[0].function_call:
    function_name = response.candidates[0].function_call.name
    function_args = response.candidates[0].function_call.arguments
    function_to_call = available_functions[function_name]
    function_response = function_to_call(**function_args)

    # Include the function response in the final output
    print(f"Function response: {function_response}")
else:
    # If no function call is needed, simply print the model's response
    print(response.candidates[0].text)