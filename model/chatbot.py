from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import google.generativeai as genai
import re

# Set up the Gemini API
GEMINI_API_KEY = "AIzaSyDdJW2e5eGpsHdLVRKKqJzuOSPKRpphWN8"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# Load access logs from JSON file
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'logs.json')
    print(f"Loading access logs from: {json_path}")
    
    with open(json_path, 'r') as file:
        access_logs = json.load(file)
    print(f"Successfully loaded {len(access_logs)} log entries")
    logs_loaded = True
except Exception as e:
    print(f"Error loading access logs: {str(e)}")
    access_logs = []
    logs_loaded = False

# Create a compact string representation of the logs for the system prompt
logs_string = json.dumps(access_logs) if logs_loaded else "[]"

SYSTEM_PROMPT = """You are a helpful assistant specializing in cybersecurity.
You will only answer questions directly related to cybersecurity.
If a question is outside of this domain, respond with 'Sorry, I can only answer questions about cybersecurity.'
Maintain context from previous turns in the conversation.
You have access to access logs data. When asked about this data, provide clear and direct answers.
Never say you don't have access to information about employees or files if it's in the access logs.

IMPORTANT FORMATTING INSTRUCTIONS:
1. Always format your responses with proper line breaks between paragraphs
2. Use bullet points (•) for lists rather than numbers
3. Use bold formatting for important information using ** symbols
4. Structure your responses with clear headings and subheadings
5. Keep sentences concise and use short paragraphs for readability
"""

# Initialize chat history
conversation_history = []
if logs_loaded:
    # Add the logs as context
    conversation_history.append({
        "role": "user", 
        "parts": [f"Here are the access logs I want you to use when answering questions: {logs_string}"]
    })
    conversation_history.append({
        "role": "model", 
        "parts": ["I've received the access logs and will use them to answer your cybersecurity questions. What would you like to know about the access patterns or security incidents?"]
    })

# Initialize the Gemini model
def get_gemini_model():
    # Using Gemini 1.5 Pro for advanced capabilities
    return genai.GenerativeModel('gemini-1.5-pro')

def get_chat_response(query):
    global conversation_history

    model = get_gemini_model()
    chat = model.start_chat(history=conversation_history)

    # Add SYSTEM_PROMPT to the beginning of the query (acting as system instruction)
    if "ajay" in query.lower() or "amar" in query.lower() or "amit" in query.lower() or "access" in query.lower() or "file" in query.lower():
        enhanced_query = f"""
{SYSTEM_PROMPT}

Question: {query}
"""
    else:
        enhanced_query = f"{SYSTEM_PROMPT}\n\n{query}"

    try:
        # Send query (without unsupported generation_config field)
        response = chat.send_message(
            enhanced_query,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 2048
            }
        )

        # Update chat history
        conversation_history.append({"role": "user", "parts": [enhanced_query]})
        conversation_history.append({"role": "model", "parts": [response.text]})

        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

app = Flask(__name__)
CORS(app)

def post_process_response(response):
    """Format the response to ensure proper styling and readability"""
    # Add line breaks if missing between paragraphs
    response = response.replace(". ", ".\n\n")
    
    # Convert numbered lists to bullet points if needed
    for i in range(1, 10):
        response = response.replace(f"{i}. ", f"• ")
    
    # Ensure bold formatting is applied to key terms
    emphasis_terms = ["unauthorized access", "security violation", "potential breach", 
                     "accessed", "suspicious", "Ajay", "Amar", "Amit", "violation"]
    
    for term in emphasis_terms:
        if term in response and f"{term}" not in response:
            response = response.replace(term, f"{term}")
    
    return response

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("query", "")
    response = get_chat_response(user_input)
    
    # Apply post-processing to improve formatting
    formatted_response = post_process_response(response)
    
    return jsonify({"response": formatted_response})

@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    
    # Re-add the logs as the first user message
    if logs_loaded:
        conversation_history.append({
            "role": "user", 
            "parts": [f"Here are the access logs I want you to use when answering questions: {logs_string}"]
        })
        conversation_history.append({
            "role": "model", 
            "parts": ["I've received the access logs and will use them to answer your cybersecurity questions. What would you like to know about the access patterns or security incidents?"]
        })
    
    return jsonify({"status": "conversation reset"})

if __name__ == "__main__":
    app.run(debug=True,port=7000)