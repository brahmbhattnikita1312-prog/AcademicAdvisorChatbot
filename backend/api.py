from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

print("API KEY:", API_KEY[:10] if API_KEY else "NOT FOUND")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set in .env"
    )

app = Flask(__name__)

# Allow all origins during development
CORS(app)

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat_proxy():

    # Handle CORS preflight request
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "No JSON received"
            }), 400

        history = data.get('history', [])

        model_name = "gemini-2.5-flash"

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model_name}:generateContent"
        )

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
            headers={
                "Content-Type": "application/json"
            }
        )

        if not response.ok:
            print("Gemini Error:", response.text)

            return jsonify({
                "error": f"Gemini API returned {response.status_code}",
                "details": response.text
            }), response.status_code

        return jsonify(response.json())

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=10000,
        debug=True
    )