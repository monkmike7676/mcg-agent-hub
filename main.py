from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI(title="mcg-agent-hub")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.get("/")
async def read_root() -> dict[str, object]:
    return {
        "message": "mcg-agent-hub is running",
        "gemini_key_loaded": bool(GEMINI_API_KEY),
    }

@app.get("/health")
async def health() -> dict[str, str | bool]:
    if not GEMINI_API_KEY:
        return {"status": "warning", "detail": "GEMINI_API_KEY not found"}
    return {"status": "ok", "detail": "GEMINI_API_KEY loaded"}
