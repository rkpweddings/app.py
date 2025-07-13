from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ✅ Replace with your actual WhatsApp API provider details
WHATSAPP_API_URL = "https://api.ultramsg.com/instance131989/"
ULTRAMSG_TOKEN = "gj5gvycjjdzwn1y0"
TO_PHONE_NUMBER = "919791811670"  # Your WhatsApp number

@app.route('/send-whatsapp', methods=['POST'])
def send_whatsapp():
    data = request.get_json()
    name = data.get("name")
    phone = data.get("phone")
    email = data.get("email")
    event_type = data.get("event_type")
    event_date = data.get("event_date")
    message = data.get("message")

    if not name or not phone:
        return jsonify({"error": "Missing name or phone"}), 400

    msg_body = (
        f"*📸 New Booking Received:*\n\n"
        f"👤 Name: {name}\n"
        f"📞 Phone: {phone}\n"
        f"📧 Email: {email}\n"
        f"🎉 Event: {event_type}\n"
        f"📅 Date: {event_date}\n"
        f"📝 Message: {message}"
    )

    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": TO_PHONE_NUMBER,
        "body": msg_body,
    }

    try:
        response = requests.post(WHATSAPP_API_URL, data=payload)
        return jsonify({"status": "success", "whatsapp_response": response.json()}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
