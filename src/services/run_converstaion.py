import sys
import requests
from openai import OpenAI
import json

sys.path.append('C:/projects/python/gpt-database-wrapper')

from src.models.handle_functions import handle_function_call
from src.models.tools import define_tools

def run_conversation(api, user_query, introduction, max_depth, GPT_API_KEY, session_messages=None):
    
    client = OpenAI(api_key=GPT_API_KEY,)
    
    if session_messages is None:
        session_messages = []

    # Start the conversation or add to it
    if not session_messages:  # This checks if the list is empty
        session_messages.append({"role": "system", "content": introduction})
    
    # Always append the user query as a new entry in the conversation
    session_messages.append({"role": "user", "content": user_query})

    # Define tools based on context
    tools = define_tools()
    
    depth = 0  # Initialize depth counter
    
    while depth < max_depth:
        # Call the GPT model with current session messages and tools
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=session_messages,
            tools=tools,
            tool_choice="auto",
        )

        # Check the finish reason of the response
        finish_reason = response.choices[0].finish_reason
        
        if finish_reason == "stop":
            # If finish_reason is 'stop', return the response and end the loop
            return response, session_messages
        elif finish_reason == "tool_calls":
            # Handle tool calls and continue the loop
            tool_calls = response.choices[0].message.tool_calls
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                function_response = handle_function_call(api, function_name, function_args)
                session_messages.append({"role": "system", "name": function_name, "content": json.dumps(function_response)})
            depth += 1  # Increment depth after each cycle
        else:
            # Continue if other reasons but log unexpected behavior
            break

    # This point should not be reached if while loop is correctly configured
    return None, session_messages

