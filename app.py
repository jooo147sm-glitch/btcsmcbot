import os
import requests
import json
from flask import Flask, request

# ====== API Keys and IDs (Hardcoded for local testing) ======
OPENAI_API_KEY = "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"
TELEGRAM_BOT_TOKEN = "8231176561:AAG-swLBZEQmUeKdhY2S1NPSc91SVlYSBeI"
TELEGRAM_CHAT_ID = "6689457582"

# ====== Flask App ======
app = Flask(__name__)

# ====== Function to Analyze BTC/USD ======
def analyze_btc_market():
    prompt = (
        "Analyze the BTC/USD market using Smart Money Concepts (SMC) and risk management "
        "principles. Provide a concise but detailed trade recommendation with entry, stop loss, and take profit."
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        data=json.dumps(data)
    )

    result = response.json()
    return result["choices"][0]["message"]["content"]

# ====== Function to Send Telegram Message ======
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=payload)

# ====== Webhook Endpoint ======
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"].strip().lower()

        if text in ["/start", "signal", "trade"]:
            analysis = analyze_btc_market()
            send_telegram_message(analysis)

    return "ok", 200

# ====== Root Endpoint ======
@app.route("/")
def home():
    analysis = analyze_btc_market()
    send_telegram_message(analysis)
    return analysis

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
