import logging
from flask import Flask, request
import requests

BOT_TOKEN = "8963386722:AAEF6MjWm1C9ik6EK9aCDFMpI5mdtvmYYY8"
CHAT_ID = "-1004487308836"

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    try:
        data = request.args if request.method == 'GET' else (request.json or request.form.to_dict())
        
        lead_holder = data.get('subid', data.get('sub_source', 'N/A'))
        conversion_id = data.get('clickid', data.get('conversion_id', 'N/A'))
        payout = data.get('payout', data.get('amount', '0.00'))
        country = data.get('country', 'N/A').upper()
        device = data.get('device', data.get('device_family', 'N/A'))
        
        message = (
            f"📢 *Account__sihab New Alert* 🚨\n\n"
            f"👤 *Lead Holder:* `{lead_holder}`\n"
            f"📦 *Conversion ID:* `{conversion_id}`\n"
            f"💲 *Payout:* `${payout}`\n"
            f"🌐 *Country:* `{country}`\n"
            f"📱 *Device:* `{device}`\n"
            f"💻 *Panel:* `Sihab-1`\n\n"
            f"✅ *Thanks_lot For This Lead* ❤️"
        )
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)
        
        return {"status": "success"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@app.route('/')
def home():
    return "Bot Server is Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
