from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from src.models.run_converstaion import run_conversation
from dotenv import load_dotenv
import os
import openai

load_dotenv()
GPT_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

@app.route('/openai-version')
def openai_version():
    return "OpenAI library version: " + openai.__version__

from functools import wraps
from flask import request, jsonify

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Retrieve the API key from the request headers
        api_key = request.headers.get('Authorization')
        
        # Check if the API key is correct
        if not api_key or api_key != os.getenv('MY_API_KEY'):
            return jsonify({"error": "Unauthorized access, invalid API key"}), 401

        return f(*args, **kwargs)
    return decorated_function


@app.route('/query', methods=['POST'])
# @require_api_key
def process_query():
    data = request.get_json()
    user_query = data.get('query')
    max_depth = data.get('max_depth', 5)
    session_messages = data.get('session_messages')
    site_id = data.get('site_id')

    from src.util.database_API_connection import ApplicationAPI

    api = ApplicationAPI(site_id)

    # Default introduction text
    default_introduction = """The system manages a database of reports and assets for various sites. Each site contains multiple assets, and each asset is linked to specific systems. 
    Reports generated for these systems contain critical data points, including severity levels that indicate the importance of the information (0=no warning, 1=early warning, 2=advanced warning).
    The API provides access to these reports, assets, and system details, enabling in-depth data analysis.
    
    As part of your response I would like you to suggest hyperlinks to different parts of the front end. Here is the EXACT LINKS:


- **Asset Information**: Use the asset ID only. Format: `http://localhost:4200/sites/summary?view=asset&asset_id={assetId}`
- **Report Information**: This requires only the report ID number. Format: `http://localhost:4200/sites/summary/{reportId}`
- **Report Data Trend Analysis**: General link, no ID required. `http://localhost:4200/sites/analytics`
- **Report Data Table Showing Most Recent Data**: General link, no ID required. `http://localhost:4200/sites/comparison`
- **Summary of All Reports for User to View**: General link, no ID required. `http://localhost:4200/sites/summary?view=total`
- **Homepage for Site**: General link, no ID required. `http://localhost:4200/sites/home`
- **Page to pick a site for analysis**: General link, no ID required. `http://localhost:4200/sites`
- **Page to see all comments**: General link, no ID required. `http://localhost:4200/sites/comments`
- **Page to upload files into**: General link, no ID required. `http://localhost:4200/sites/upload`


    Please as much as possible use EXACT HYPERLINKS to guide to user to more information on the site.

    """

    # Use provided introduction if available, otherwise use the default
    GPT_Introduction = data.get('introduction', default_introduction)

    # Running the conversation function from utils
    response, session_messages = run_conversation(api, user_query, GPT_Introduction, max_depth, GPT_API_KEY, session_messages)

    # Formatting the final message content for output
    message_content = response['choices'][0]['message']['content'] if response else "No response generated."

    return jsonify({
        "response": message_content,
        "conversation": session_messages
    })

if __name__ == "__main__":
    app.run(port=3060)
