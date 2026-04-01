# 🤖 TechCorp AI Customer Support Chatbot

> A production-ready AI-powered customer support chatbot built with **FastAPI**, **Groq (LLaMA 3.3-70B)**, and vanilla JavaScript. Features real-time streaming responses, bilingual support (EN/TR), and persistent conversation memory.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-FF6B35?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- ⚡ **Streaming responses** — Token-by-token output via Server-Sent Events (SSE), no waiting
- 🧠 **Conversation memory** — Full chat history sent per request, context-aware replies
- 🌍 **Bilingual (EN / TR)** — UI and AI responses adapt to user's language automatically
- 🎭 **Custom AI persona** — "Aria" represents TechCorp with product knowledge built into the system prompt
- 🚀 **Groq-powered** — Ultra-fast inference using LLaMA 3.3-70B Versatile (free tier available)
- 🔌 **REST API** — Clean `/chat/stream` endpoint, easy to integrate into any frontend
- 🎨 **Modern UI** — Dark-themed, responsive chat interface with typing indicators

---

## 🏗 Architecture

```
┌──────────────────────┐        SSE Stream        ┌──────────────────────┐
│   Frontend           │ ◄──────────────────────► │   FastAPI Backend    │
│   (HTML/CSS/JS)      │   POST /chat/stream       │   (main.py)          │
│                      │                           │                      │
│  - Chat UI           │                           │  - Groq API client   │
│  - Streaming render  │                           │  - System prompt     │
│  - History tracking  │                           │  - SSE generator     │
│  - Lang switcher     │                           │  - CORS middleware   │
└──────────────────────┘                           └──────────┬───────────┘
                                                              │
                                                              ▼
                                                   ┌──────────────────────┐
                                                   │   Groq Cloud API     │
                                                   │   LLaMA 3.3-70B      │
                                                   └──────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/techcorp-chatbot.git
cd techcorp-chatbot
```

### 2. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Set up your Groq API key

Get a free API key at [console.groq.com](https://console.groq.com)

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

Or create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the backend

```bash
uvicorn main:app --reload --port 8000
```

### 5. Open the frontend

Simply open `frontend/index.html` in your browser — or serve it:

```bash
cd ../frontend
python -m http.server 5500
```

Navigate to `http://localhost:5500`

---

## 📁 Project Structure

```
techcorp-chatbot/
├── backend/
│   ├── main.py            # FastAPI app, Groq streaming, CORS
│   └── requirements.txt   # Python dependencies
├── frontend/
│   └── index.html         # Full chat UI (HTML + CSS + JS)
└── README.md
```

---

## 🔌 API Reference

### `POST /chat/stream`

Streams AI responses as Server-Sent Events.

**Request body:**
```json
{
  "messages": [
    { "role": "user", "content": "What plans do you offer?" },
    { "role": "assistant", "content": "We offer three plans..." },
    { "role": "user", "content": "Tell me more about the Pro plan" }
  ]
}
```

**Response (SSE stream):**
```
data: {"content": "The"}
data: {"content": " Pro"}
data: {"content": " plan"}
data: [DONE]
```

### `GET /health`

Returns API health status.

```json
{ "status": "healthy" }
```

---

## 🛠 Customization

To adapt this chatbot for your own business, edit the `SYSTEM_PROMPT` in `backend/main.py`:

```python
SYSTEM_PROMPT = """You are [Your Bot Name], [Your Company]'s support assistant.

[Your Company] offers:
- Product A: ...
- Product B: ...

Key info:
- Support email: ...
- Pricing: ...
"""
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI, Uvicorn |
| AI Model | LLaMA 3.3-70B via Groq API |
| Streaming | Server-Sent Events (SSE) |
| Frontend | HTML5, CSS3, Vanilla JS |
| Fonts | Syne, DM Mono (Google Fonts) |

---

## 📄 License

MIT — free to use, modify, and deploy.

---

## 🤝 Contact

Built by [Murat Yesilyurt] — available for freelance AI/chatbot projects on [Upwork](https://www.upwork.com/freelancers/~01e45f433b6bc60914).
