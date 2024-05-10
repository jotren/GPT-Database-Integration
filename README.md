# Overview

We are trying to create a model that will integrate with existing APIs and then be able to summarise and answer questions about the data. First step was to script a verison of the model that can work. You can see this script in "workbooks".

### Database

Using a database that provides information on oil reports for a number of assets at a site. There is lots of information here about assset health. Will integrate a LLM that is able to "speak" to this database and answer specific questions.

### GPT Setup

Used the OpenAI chat GPT API to run this model. This API has callable functions, where you feed the API a list of "tools" which represent functions and then asking the GPT to pick the relevant function:

```python

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0125",
    messages=session_messages,
    tools=tools,
    tool_choice="auto", # Allow the GPT to select any tools
)
```
The structure of these tools is so:

```python 
def define_tools():
    tools = []

    # Adding other fixed tools to the list
    tools.append({
        "type": "function",
        "function": {
            "name": "get_all_system_severity_data",
            "description": "Fetch high level details on the severities of all the systems in the site. Severity2 is advanced warning, Severity1 is early warning, and Severity0 is no warning.",
            "parameters": {},
        }
    })

```
These "tools" represent names of API endpoints. Once the GPT picked the API endpoint, the function would be called and the data returned for the next iteration. For example:
Then we feed this name into the function handler: 

```python
def handle_function_call(function_name, function_args):
    try:
        if function_name == "get_asset_ids_names":
            asset_data = api.get_asset_ids_names()
            function_response = asset_data        
        # Plus other functions

    return function_response
function_name = tool_call.function.name
```
Once we had this system in place we could call the database.

### GPT Database Integration

Initial system allowed us to query the database, but only with very simple queries.

Initial challenge was getting the GTP to "daisy-chain" functions so that multiple functions can be called to bring disperate pieces of information together and answer complex questions. This was solved through __recursion__:

```python
    depth = 0  # Initialize depth counter
    while depth < max_depth:
        # Call the GPT model with current session messages and tools
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=session_messages,
            tools=tools,
            tool_choice="auto",
        )

        # Check the finish reason of the response
        finish_reason = response.choices[0]['finish_reason']
        print(f'Response with finish_reason = {finish_reason}')
        
        if finish_reason == "stop":
            # If finish_reason is 'stop', return the response and end the loop
            return response, session_messages
        elif finish_reason == "tool_calls":
            # Handle tool calls and continue the loop
            tool_calls = response.choices[0].message['tool_calls']
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                function_response = handle_function_call(function_name, function_args)
                print(f'Response from {function_name}:', function_response)
                session_messages.append({"role": "system", "name": function_name, "content": json.dumps(function_response)})
            depth += 1  # Increment depth after each cycle
        else:
            # Continue if other reasons but log unexpected behavior
            print(f'Unhandled finish reason: {finish_reason}')
            break

```
The algorithm  will continue to run until in the while loop until it feels it has enough data. The while loop checks the:

```python
finish_reason = response.choices[0]['finish_reason']
```
This contains information on whether another tool was called or the algorithmn has generated a resonse. Once this is done, the application will then return the response.

### GPT Deployment

Once this was discovered we then used __FLASK__ to expose this Bot to requests: 

```python
@app.route('/query', methods=['POST'])
@require_api_key
def process_query():
    data = request.get_json()
    user_query = data.get('query')
    max_depth = data.get('max_depth', 5)
    session_messages = data.get('session_messages')

    # Default introduction text
    default_introduction = """Intro"""

    # Use provided introduction if available, otherwise use the default
    GPT_Introduction = data.get('introduction', default_introduction)

    # Running the conversation function from utils
    response, session_messages = run_conversation(user_query, GPT_Introduction, max_depth, GPT_API_KEY, session_messages)

    # Formatting the final message content for output
    message_content = response['choices'][0]['message']['content'] if response else "No response generated."

    return jsonify({
        "response": message_content,
        "conversation": session_messages
    })

```