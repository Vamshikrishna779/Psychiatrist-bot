import os
import requests
from flask import Flask, jsonify, send_from_directory, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Set your API details (ensure you have set the GEMINI_API_KEY in .env file)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"

def ask_gemini(prompt):
    try:
        # Add identity context to the prompt
        context = "You are Psychiatrist Bot, an AI mental health support assistant. " \
                 "Provide empathetic, supportive responses to users discussing mental health. " \
                 "Always identify yourself as Psychiatrist Bot. " \
                 "Never claim to be a real doctor or therapist. " \
                 "Here is the user's message: "
        
        full_prompt = context + prompt
        
        response = requests.post(
            GEMINI_API_URL,
            json={"contents": [{"parts": [{"text": full_prompt}]}]},
            params={"key": GEMINI_API_KEY}
        )
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"API Error: {str(e)}"

@app.route('/')
def home():
    # Serve the index.html from the root folder (no need for templates directory)
    return send_from_directory('.', 'index.html')

@app.route('/get', methods=['POST'])
def get_bot_response():
    user_input = request.json.get("message").lower().strip()
    
    # Direct response for identity questions
    if user_input in ["who are you", "what are you"]:
        return jsonify({
            "response": "I'm Psychiatrist Bot, an AI assistant here to provide mental health support and information. " \
                        "While I'm not a human therapist, I'm here to listen and offer resources that might help."
        })
    
    response = ask_gemini(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
