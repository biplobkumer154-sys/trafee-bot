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

    payout = data.get("sum") or data.get("payout") or "0.00"
    country = data.get("country", "N/A").upper()
    ip_address = data.get("ext_click_id") or request.remote_addr or "N/A"
    smartlink_name = data.get("name", "CONGRATTULATIONS_NEW")

    # Device detection logic
    device = data.get("device")
    if not device or device == "N/A" or device == "":
      user_agent = request.headers.get("User-Agent", "").lower()
      if "iphone" in user_agent or "ipad" in user_agent:
        device = "iPhone"
      elif "android" in user_agent:
        device = "Android"
      elif "windows" in user_agent or "macintosh" in user_agent:
        device = "Desktop"
      else:
        device = "Mobile"

    # Your preferred message format
    message = (
        f"🎁 *{smartlink_name}* 🎁\n\n"
        f"🆔: `{lead_holder}`\n"
        f"🌐: `{country}`\n"
        f"💲: `{payout}`\n"
        f"📱: `{device}`\n"
        f"🟥: `{ip_address}`\n"
        f"🗼: `Mobile`"
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
