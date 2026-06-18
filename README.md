# Rowan University Academic Advisor Chatbot

A web-based chatbot that helps Rowan University students with course selection, major requirements, and academic planning. Uses a small Flask backend to proxy requests to the Google Gemini API, so your API key never lives in the browser.

## Features

- 🤖 AI-powered academic advisor assistant
- 📚 Course selection guidance
- 🎓 Major requirements explanation
- 📅 Academic planning assistance
- 💬 Interactive chat interface
- ⚡ Quick prompt buttons for common questions

## Architecture

- `index.html` + `app.js` — React frontend (no build step, loaded via CDN scripts)
- `api.py` — Flask backend that proxies chat requests to the Gemini API using your server-side API key

The frontend never talks to Google directly; it calls your local Flask server at `http://127.0.0.1:5001/api/chat`, which forwards the request to Gemini using the key from your `.env` file.

## 🧠 System Architecture

User Input (Frontend)
        ↓
Flask Backend (API Proxy)
        ↓
Google Gemini API
        ↓
AI Response returned to UI


## 🛠️ Tech Stack

**Frontend:**
- HTML
- JavaScript
- Tailwind CSS

**Backend:**
- Python
- Flask
- Flask-CORS

**AI:**
- Google Gemini API


## Setup

### 1. Get a Gemini API key

Get a key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Configure the backend

Create a `.env` file next to `api.py` and paste in your key:

git add README.md
git commit -m "Add live demo link"
git push

## Live Demo
https://academicchatbotniki.netlify.app