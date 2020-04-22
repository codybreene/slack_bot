import os
from flask import Flask, request, Response

#instantiate app
app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')

@app.route('/slack', methods=['POST'])
def inbound():
  if request.form.get('token') == SLACK_WEBHOOK_SECRET:
    channel = request.form.get('channel_name')
    username = request.form.get('user_name')
    text = request.form.get('text')
    inbound = "User: " + username


