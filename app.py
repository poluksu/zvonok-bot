from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

sent_call_ids = set()

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data, timeout=10)

@app.route("/", methods=["GET"])
def home():
    return "OK", 200

@app.route("/zvonok", methods=["GET", "POST"])
def zvonok_webhook():
    data = request.values

    call_id = data.get("ct_call_id", "")
    phone = data.get("ct_phone", "неизвестно")
    campaign_id = data.get("ct_campaign_id", "без ID")
    button_num = data.get("ct_button_num", "")

    if button_num == "1":
        if call_id and call_id not in sent_call_ids:
            sent_call_ids.add(call_id)

            text = (
                f"Новая заявка из Звонка\n"
                f"Кампания ID: {campaign_id}\n"
                f"Номер: {phone}"
            )
            send_telegram_message(text)

    return "OK", 200
