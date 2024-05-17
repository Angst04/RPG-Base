from aiogram import Router

from fastapi import FastAPI, Request
import uvicorn
from starlette.middleware.cors import CORSMiddleware

router = Router()

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

@app.post("/api/send_card")
async def receive_data(request: Request):
   data = await request.json()
   user_id = data['user_id']
   card_id = data['card_id']
   await router.send_message(user_id, f"Получены данные из веб-приложения: {card_id}")
   return {"status": "ok"}

def start_web():
   uvicorn.run(app, host='0.0.0.0', port=8000)