#------------------------------------
# Backend Rest API, przygotowany do współpracy z frontendem front_end_fast_api.py
#------------------------------------

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os
from fastapi.middleware.cors import CORSMiddleware
import logging

load_dotenv()
app = FastAPI()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY_TEST = os.getenv("GROQ_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

class ChatRequest(BaseModel):
    message: str
    creativity: float
    model: str 

#Logging configuration
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message can not be empty.")
    
    if not GROQ_API_KEY_TEST:
        raise HTTPException(status_code=500, detail="Groq API key is missing.")
    
    try:
        response = requests.post(
            GROQ_API_URL,
            headers = {"Authorization": f"Bearer {GROQ_API_KEY_TEST}", "Content-Type": "application/json"},
            json = {"messages": [{"role": "user", "content": request.message}], "temperature": request.creativity, "model": request.model},
        )
        response.raise_for_status()
        logger.info(f"✅ API Response: {response.json()}")
        data = response.json()
        ai_response = data["choices"][0]["message"]["content"]
    except request.exceptions.RequestException as e:
        logger.error(f"❌ Error contacting GROQ API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error contacting GROQ API: {str(e)}")
    
    return {"response": ai_response}

@app.get("/")
def read_root():
    return {"message": "Chatbot API is running"}