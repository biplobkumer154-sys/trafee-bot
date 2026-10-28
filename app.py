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

    # Tracking parameter theke name/ID dhorar jonno
    lead_holder = (
        data.get("track")
        or data.get("sub_source")
        or data.get("ext1")
        or data.get("name")
        or "Rakib"
    )

    country = data.get("country", "N/A").upper()
    currency = data.get("currency", "USD")
    sum_payout = data.get("sum") or data.get("payout") or "0.00"
    sale_time = data.get("sale_time", "N/A")
    smartlink_name = data.get("name", "CONGRATTULATIONS_NEW")
    ext_click_id = data.get("ext_click_id", "N/A")
    transaction_id = data.get("transaction_id", "N/A")
    int_click_id = data.get("int_click_id", "N/A")
    adv_tid = data.get("adv_tid", "N/A")
    ext1 = data.get("ext1", "N/A")
    ext2 = data.get("ext2", "N/A")
    ext3 = data.get("ext3", "N/A")

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

    # Screen shot onujayi shob parameter soho message format
    message = (
        f"🎁 *{smartlink_name}* 🎁\n\n"
        f"🆔: `{lead_holder}`\n"
        f"🌐: `{country}`\n"
        f"💰: `{sum_payout} {currency}`\n"
        f"📱: `{device}`\n"
        f"🕒: `{sale_time}`\n"
        f"🟥: `{ext_click_id}`\n"
        f"🆔 Tx: `{transaction_id}`\n"
        f"🔗 Ext1: `{ext1}`\n"
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
