# 🌐 LexiBridge — Language Translation Tool

Free, open-source translation tool with FastAPI backend and vanilla HTML frontend.

## Tech Stack
- **Backend**: Python 3.11+, FastAPI 0.115, deep-translator, langdetect
- **Frontend**: HTML5, CSS3, Vanilla JS, Web Speech API (TTS)
- **Translation**: Google Translate (via deep-translator — no API key needed)

## Project Structure
```
translation-tool/
├── backend/
│   ├── main.py            # FastAPI app
│   └── requirements.txt   # Python dependencies
├── frontend/
│   └── index.html         # Complete UI
└── README.md
```

## Setup & Run

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Backend runs at: http://localhost:8000
API Docs at:     http://localhost:8000/docs

### 2. Frontend
Open `frontend/index.html` directly in your browser.
(No server needed — it's pure HTML/JS)

## API Endpoints
| Method | Endpoint     | Description               |
|--------|--------------|---------------------------|
| GET    | /            | Health check              |
| GET    | /languages   | List all supported langs  |
| POST   | /translate   | Translate text            |
| GET    | /detect?text=| Detect language           |

## Features
- ✅ 70+ languages supported
- ✅ Auto language detection
- ✅ Swap source ↔ target languages
- ✅ Copy translation to clipboard
- ✅ Text-to-speech (source & translated)
- ✅ Character counter (5000 limit)
- ✅ Session stats (translations, characters)
- ✅ Keyboard shortcut: Ctrl+Enter to translate
- ✅ No API key required