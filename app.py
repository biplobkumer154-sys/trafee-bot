import os
import requests
from flask import Flask, request

BOT_TOKEN = "8963386722:AAEF6MjWm1C9ik6EK9aCDFMpI5mdtvmYYY8"
CHAT_ID = "-1004487308836"

app = Flask(__name__)


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
  try:
    data = (
        request.args
        if request.method == "GET"
        else (request.json or request.form.to_dict())
    )

    # Capturing the name/sub-id from tracking parameters
    lead_holder = (
        data.get("track")
        or data.get("sub_source")
        or data.get("ext1")
        or data.get("name")
        or "Rakib"
    )

    conversion_id = (
        data.get("transaction_id") or data.get("clickid") or "N/A"
    )
    payout = data.get("sum") or data.get("payout") or "0.00"
    country = data.get("country", "N/A").upper()
    smartlink_name = data.get("name", "Adult dating 1")

    # Device detection logic to prevent showing literal '{device}'
    device = data.get("device")
    if not device or device == "N/A" or device == "" or "{" in device:
      user_agent = request.headers.get("User-Agent", "").lower()
      if "iphone" in user_agent or "ipad" in user_agent:
        device = "iPhone"
      elif "android" in user_agent:
        device = "Android"
      elif "windows" in user_agent or "macintosh" in user_agent:
        device = "Desktop"
      else:
        device = "Mobile"

    # Your exact requested message format
    message = (
        f"📢 *Account__sihab New Alert* 🚨\n\n"
        f"👤 *Lead Holder:* `{lead_holder}`\n"
        f"📦 *Conversion ID:* `{conversion_id}`\n"
        f"💲 *Payout:* `${payout}`\n"
        f"🌐 *Country:* `{country}`\n"
        f"📱 *Device:* `{device}`\n"
        f"🏷️ *Smartlink:* `{smartlink_name}`\n"
        f"💻 *Panel:* `Sihab-1`\n\n"
        f"✅ *Thanks_lot For This Lead* ❤️"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

    return {"status": "success"}, 200
  except Exception as e:
    return {"status": "error", "message": str(e)}, 400


@app.route("/")
def home():
  return "Bot Server is Running!"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
