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
    print("[DEBUG] Data received:", data)

    payload = {
        "to": WHATSAPP_TO,
        "body": f"""📸 New Booking

Name: {data.get('name')}
Phone: {data.get('phone')}
Email: {data.get('email')}
Event Type: {data.get('event_type')}
Event Date: {data.get('event_date')}
Message: {data.get('message')}
"""
    }

    url = f"https://api.ultramsg.com/{ULTRA_INSTANCE_ID}/messages/chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ULTRA_TOKEN}"
    }

    print("[DEBUG] Sending to URL:", url)
    print("[DEBUG] Payload:", payload)

    response = requests.post(url, json=payload, headers=headers)
    print("[DEBUG] WhatsApp API Response:", response.status_code, response.text)

    if response.status_code == 200:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": response.text}), 500


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
