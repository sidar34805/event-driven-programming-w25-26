import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Bu bilgileri Railway'den çekecek
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

class QuizResult(BaseModel):
    student_name: str
    score: str

@app.get("/")
def read_root():
    return {"message": "Quiz Bot Çalışıyor! 🚀"}

@app.post("/send-result")
def send_quiz_result(result: QuizResult):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise HTTPException(status_code=500, detail="Telegram ayarları eksik!")
    
    message = f"📢 *Quiz Tamamlandı!*\n\n👤 **Öğrenci:** {result.student_name}\n🏆 **Skor:** {result.score}"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        return {"status": "error", "detail": response.text}
        
    return {"status": "success", "message": "Mesaj Telegram'a gitti!"}
