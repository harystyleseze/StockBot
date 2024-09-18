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
    """
    Send a message using Twilio API to the recipient's WhatsApp number.
    
    Args:
        msg (str): The message content to be sent.
        recipient (str): The recipient's WhatsApp number in E.164 format (e.g., 'whatsapp:+1234567890').
    """
    try:
        # Send the message through the Twilio client
        client.messages.create(
            from_=TWILIO_NUMBER,
            body=msg,
            to=recipient
        )
    except Exception as e:
        # Log an error message if sending the message fails
        app.logger.error(f"Failed to send message: {str(e)}")

def process_msg(msg):
    """
    Process incoming WhatsApp messages and determine the appropriate response.
    
    Args:
        msg (str): The message received from the user.
    
    Returns:
        str: The response message to be sent back to the user.
    """
    response = "" # Initialize the response message
    
    # Check if the user is greeting with "Hi"
    if msg.strip() == "Hi":
        response = ("Hello, welcome to the Stock Market bot! "
                    "Type sym:<stock_symbol> to know the price of the latest stock.")
    # Check if the user is requesting stock information with "sym:<stock_symbol>"
    elif msg.lower().startswith('sym:'):
        data = msg.split(':', 1)

        # Validate the message format
        if len(data) < 2 or not data[1].strip():
            response = "Invalid format. Please use sym:<stock_symbol>."
        else:
            stock_symbol = data[1].strip()
            try:
                # Fetch the stock price using the MarketStack API
                stock_price = get_stock_price(stock_symbol)
                last_price = stock_price.get('last_price', 'N/A')
                response = f"The stock price of {stock_symbol} is: ${last_price}"
            except Exception as e:
                # Handle any errors from the API call
                response = f"{str(e)}"
    # If the input does not match any recognized pattern
    else:
        response = "Invalid input. Please type 'Hi' to get started or use the format sym:<stock_symbol> to get stock prices."
    return response

@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Handle incoming messages from Twilio's WhatsApp webhook and respond accordingly.
    
    This function receives the user's message and sender's details from the webhook,
    processes the message, and sends an appropriate response via Twilio's API.
    
    Returns:
        JSON response indicating the status of the operation.
    """
    f = request.form # Get the incoming form data from the POST request
    msg = f.get('Body', '').strip() # Extract the message body
    sender = f.get('From', '') # Extract the sender's WhatsApp number

    # Log the incoming message and sender for debugging purposes
    app.logger.info(f"Received message: {msg} from {sender}")

    # Validate that both the message and sender are provided
    if not msg or not sender:
        return jsonify({"error": "Missing parameters"}), 400 # Return an error if any parameters are missing

    # Process the incoming message and generate a response
    response = process_msg(msg)

    # Send the generated response back to the user
    send_msg(response, sender)

    # Return a success response to indicate that the webhook handled the message
    return jsonify({"status": "OK"}), 200

if __name__ == "__main__":
    # Run the Flask application on port 5001, accessible from any host (0.0.0.0)
    app.run(host="0.0.0.0", port=5001, debug=False)
