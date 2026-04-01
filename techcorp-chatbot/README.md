# 🤖 TechCorp AI Customer Support Chatbot

A production-ready, streaming AI customer support chatbot built with **FastAPI**, **Groq (LLaMA 3.3 70B)**, and a clean vanilla frontend. Designed as a real-world SaaS support assistant with full bilingual support.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## ✨ Features

| Feature | Details |
|---|---|
| ⚡ **Streaming responses** | Token-by-token output via Server-Sent Events |
| 🧠 **Conversation memory** | Full multi-turn chat history per session |
| 🌍 **Bilingual** | Auto-detects Turkish & English, responds accordingly |
| 🎯 **Domain-specific** | Custom system prompt with real product/pricing knowledge |
| 🏗️ **Production-ready** | CORS, error handling, health endpoint, env config |
| 🎨 **Modern UI** | Dark-mode chat interface with typing cursor animation |

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn, HTTPX
- **AI**: Groq Cloud API — `llama-3.3-70b-versatile`
- **Frontend**: Vanilla HTML/CSS/JS (zero dependencies, zero build step)
- **Protocol**: Server-Sent Events (SSE) for real-time streaming

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/techcorp-ai-support.git
cd techcorp-ai-support
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
# Get a free key at: https://console.groq.com
```

### 4. Run
```bash
uvicorn main:app --reload
```

Open http://localhost:8000 — done! 🎉

---

## 📁 Project Structure

```
techcorp-ai-support/
├── main.py              # FastAPI app — routes, streaming logic, system prompt
├── static/
│   └── index.html       # Full chat UI (HTML + CSS + JS, single file)
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔌 API Reference

### POST /chat
Send a message and receive a streaming SSE response.

Request body:
```json
{
  "messages": [
    { "role": "user", "content": "What plans do you offer?" }
  ]
}
```

Response: text/event-stream
```
data: {"content": "We offer three plans..."}
data: [DONE]
```

### GET /health
Returns service status and model info.

---

## 🧩 Customization

To adapt this chatbot for any business:

1. Edit SYSTEM_PROMPT in main.py — add your company info, products, FAQs
2. Update suggestion buttons in static/index.html
3. Swap the model — any Groq-supported model works
4. Add authentication — wrap endpoints with OAuth2/API key middleware

---

## 📄 License

MIT — free to use and adapt for commercial projects.

---

## 👤 Author

Built by [Your Name] — available for freelance AI/chatbot projects on Upwork.
