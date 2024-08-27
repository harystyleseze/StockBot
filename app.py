from flask import Flask
from flask import request
from twilio.rest import Client
import os

app = Flask(__name__)

ACCOUNT_ID = os.environ.get('TWILIO_ACCOUNT')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')
TWILIO_NUMBER = 'whatsapp:+14155238886'

client = Client(ACCOUNT_ID, TWILIO_TOKEN)

def send_msg(msg, recipient):
    client.messages.create(
        from_=TWILIO_NUMBER,
        body=msg,
        to=recipient
    )

def process_msg(msg):
    response = ""
    if msg == "Hi":
        response = "Hello, welcome to the Stock Market bot!"
    else:
        response = "Please type hi to get started."
    return response

@app.route("/webhook", methods=["POST"])
def webhook():
    f = request.form
    msg = f['Body']
    sender = f['From']
    response = process_msg(msg)
    send_msg(response, sender)
    return "OK", 200
