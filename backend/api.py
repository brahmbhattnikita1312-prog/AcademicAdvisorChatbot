from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
print("API KEY:", API_KEY[:10] if API_KEY else "NOT FOUND") #

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Create a .env file next to api.py "
        "with a line like: GEMINI_API_KEY=your_key_here"
    )

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "http://localhost:8080",
            "http://127.0.0.1:8080",
            "null"  # allows index.html opened directly via file://
        ]
    }
}) 

@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    try:
        data = request.json
        if not data or 'history' not in data:
            return jsonify({"error": "Request body must include 'history'"}), 400

        history = data.get('history', [])
        
        # Fixed: Updated to an active model
        model_name = "gemini-2.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        
        payload = {
            "contents": history,
            "generationConfig": {
                "maxOutputTokens": 1000,
                "temperature": 0.7
            }
        }

        response = requests.post(
            url, 
            json=payload, 
            params={"key": API_KEY}, 
            headers={"Content-Type": "application/json"}
        )

        if not response.ok:
            print(f"Gemini API error {response.status_code}: {response.text}")
            return jsonify({
                "error": f"Gemini API returned {response.status_code}",
                "details": response.text
            }), response.status_code

        return jsonify(response.json())

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
#if __name__ == '__main__':
#   app.run(host='127.0.0.1', port=5001, debug=True)