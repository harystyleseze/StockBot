from flask import Flask, request, jsonify
from twilio.rest import Client
from marketstack import get_stock_price
import os

app = Flask(__name__)

"""Retrieve Twilio credentials from environment variables"""
ACCOUNT_ID = os.environ.get('TWILIO_ACCOUNT', 'your_default_account_id')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN', 'your_default_token')
client = Client(ACCOUNT_ID, TWILIO_TOKEN)
TWILIO_NUMBER = 'whatsapp:+14155238886'

def send_msg(msg, recipient):
    """Send a message using Twilio API."""
    try:
        client.messages.create(
            from_=TWILIO_NUMBER,
            body=msg,
            to=recipient
        )
    except Exception as e:
        app.logger.error(f"Failed to send message: {str(e)}")

def process_msg(msg):
    """Process incoming messages and return appropriate responses."""
    response = ""
    if msg.strip() == "Hi":
        response = ("Hello, welcome to the Stock Market bot! "
                    "Type sym:<stock_symbol> to know the price of the latest stock.")
    elif msg.lower().startswith('sym:'):
        data = msg.split(':', 1)
        if len(data) < 2 or not data[1].strip():
            response = "Invalid format. Please use sym:<stock_symbol>."
        else:
            stock_symbol = data[1].strip()
            try:
                stock_price = get_stock_price(stock_symbol)
                last_price = stock_price.get('last_price', 'N/A')
                response = f"The stock price of {stock_symbol} is: ${last_price}"
            except Exception as e:
                response = f"{str(e)}"
    else:
        response = "Invalid input. Please type 'Hi' to get started or use the format sym:<stock_symbol> to get stock prices."
    return response

@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle incoming messages from Twilio webhook."""
    f = request.form
    msg = f.get('Body', '').strip()
    sender = f.get('From', '')

    """Log incoming request for debugging"""
    app.logger.info(f"Received message: {msg} from {sender}")

    if not msg or not sender:
        return jsonify({"error": "Missing parameters"}), 400

    response = process_msg(msg)
    send_msg(response, sender)
    return jsonify({"status": "OK"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
