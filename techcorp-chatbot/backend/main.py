from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import os
from groq import Groq

app = FastAPI(title="TechCorp Customer Support API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are Aria, TechCorp's intelligent customer support assistant.

TechCorp is a SaaS company offering:
- ProjectFlow: Project management platform (Free, Pro $29/mo, Enterprise $99/mo)
- DataSync: Real-time data integration tool
- CloudDeploy: One-click cloud deployment solution

Key info:
- Support: support@techcorp.io | Available 24/7
- Docs: docs.techcorp.io
- Free trial: 14 days, no credit card required
- Refund policy: 30-day money-back guarantee

Guidelines:
- Detect the user's language and respond in the SAME language (Turkish or English)
- Be warm, concise, and helpful
- For complex technical issues, offer to escalate to human support
- Never make up information not listed above
- If unsure, say so and offer to connect with a human agent
"""

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.get("/")
def root():
    return {"status": "TechCorp Support API is running", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += [{"role": m.role, "content": m.content} for m in request.messages]

    def generate():
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                stream=True,
                max_tokens=1024,
                temperature=0.7,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield f"data: {json.dumps({'content': delta})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )
