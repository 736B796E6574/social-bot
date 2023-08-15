from flask import Flask, request, jsonify
import hashlib
import hmac
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')  # You choose this and set it in the Facebook dashboard
PAGE_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification request from Facebook
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                return challenge, 200
        return 'Verification Failed', 403

    elif request.method == 'POST':
        # Actual webhook event
        data = request.json
        if data['object'] == 'page':
            for entry in data['entry']:
                for event in entry['messaging']:
                    sender_id = event['sender']['id']
                    send_reply(sender_id, "you smell")

        return 'EVENT_RECEIVED', 200

def send_reply(user_id, message_text):
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "recipient": {
            "id": user_id
        },
        "message": {
            "text": message_text
        }
    }

    response = requests.post(f"https://graph.facebook.com/v12.0/me/messages?access_token={PAGE_ACCESS_TOKEN}", 
                             headers=headers, 
                             json=payload)

    return response.json()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
