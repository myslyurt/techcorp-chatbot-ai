from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json
import httpx

app = FastAPI(title="TechCorp AI Support", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are Aria, TechCorp's friendly and professional AI customer support assistant.

TechCorp is a SaaS company offering:
- CloudSync Pro: Real-time cloud storage & collaboration ($29/mo per team)
- DataPulse Analytics: Business intelligence dashboard ($49/mo)
- SecureVault: Enterprise security & compliance tools ($99/mo)
- API Connect: Developer API platform (pay-as-you-go)

Key support info:
- Free 14-day trial on all plans, no credit card required
- Cancel anytime, no hidden fees
- 24/7 support via chat, email (support@techcorp.io), and phone (+1-800-TECHCORP)
- 99.9% uptime SLA guarantee
- SOC2 Type II & GDPR compliant
- Refunds within 30 days of purchase

Behavior rules:
- Detect the user's language automatically (Turkish or English) and ALWAYS respond in the same language
- Be concise, warm, and solution-focused
- For billing/account issues, ask for their email and tell them a human agent will follow up
- Never make up features or pricing not listed above
- If unsure, say so and offer to escalate to a human agent
"""

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    session_id: Optional[str] = None

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/chat")
async def chat(request: ChatRequest):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in request.messages:
        messages.append({"role": msg.role, "content": msg.content})

    async def stream_response():
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST",
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": MODEL,
                    "messages": messages,
                    "stream": True,
                    "max_tokens": 1024,
                    "temperature": 0.7,
                },
            ) as response:
                if response.status_code != 200:
                    error_body = await response.aread()
                    yield f"data: {json.dumps({'error': f'Groq API error: {response.status_code}'})}\n\n"
                    return

                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            yield "data: [DONE]\n\n"
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk["choices"][0]["delta"]
                            if "content" in delta and delta["content"]:
                                yield f"data: {json.dumps({'content': delta['content']})}\n\n"
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue

    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )

@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL, "service": "TechCorp AI Support"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
