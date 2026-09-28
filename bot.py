import requests
import os

from dotenv import load_dotenv
from calendar_service import get_today_events, create_daily_message

load_dotenv()

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

def send_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data, timeout=10)

    return response.json()


events = get_today_events()

message = create_daily_message(events)

send_message(message)