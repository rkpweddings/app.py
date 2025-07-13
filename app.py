from flask import Flask, request, jsonify
import smtplib
import requests
import os

app = Flask(__name__)

# ✅ Load environment variables
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
ULTRA_INSTANCE_ID = os.environ.get("ULTRA_INSTANCE_ID")
ULTRA_TOKEN = os.environ.get("ULTRA_TOKEN")
WHATSAPP_TO = os.environ.get("WHATSAPP_TO")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is working"}), 200

@app.route("/send-whatsapp", methods=["POST"])
def send_whatsapp():
    data = request.json
    name = data.get("name")
    phone = data.get("phone")
    email = data.get("email")
    event_type = data.get("event_type")
    event_date = data.get("event_date")
    message = data.get("message")

    whatsapp_message = (
        f"📸 New Booking Received!\n"
        f"👤 Name: {name}\n"
        f"📞 Phone: {phone}\n"
        f"📧 Email: {email}\n"
        f"🎉 Event Type: {event_type}\n"
        f"📅 Event Date: {event_date}\n"
        f"📝 Message: {message}"
    )

    # ✅ WhatsApp via UltraMsg
    try:
        whatsapp_url = f"https://api.ultramsg.com/{ULTRA_INSTANCE_ID}/messages/chat"
        payload = {
            "token": ULTRA_TOKEN,
            "to": WHATSAPP_TO,
            "body": whatsapp_message
        }
        res = requests.post(whatsapp_url, data=payload)
        print("✅ WhatsApp response:", res.text)
    except Exception as e:
        print("❌ WhatsApp error:", e)

    # ✅ Send email
    try:
        subject = "New Photography Booking"
        email_message = f"Subject: {subject}\n\n{whatsapp_message}"
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, email_message)
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Email error:", e)

    return jsonify({"message": "Booking notification sent"}), 200

if __name__ == "__main__":
    app.run(debug=True)
