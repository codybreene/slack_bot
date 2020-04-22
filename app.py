import os
import logging
logging.basicConfig(level=logging.DEBUG)

from flask import Flask, request, Response
from slack import WebClient
from slack.errors import SlackApiError
from slackeventsapi import SlackEventAdapter

#instantiate app
app = Flask(__name__)

events_adapter = SlackEventAdapter(
    os.environ['SLACK_SIGNING_SECRET'], endpoint="/events", server=app)
client = WebClient(os.environ['BOT_TOKEN'])

phrases = []

def send_message(id, message):
  try:
    response = client.chat_postMessage(
      channel=id,
      text=message
    )
  except SlackApiError as e:
    assert e.response["error"]

@events_adapter.on("message")
def handle_message(event_data):
  message = event_data["event"]
  if "yolo" in message.get('text'):
    user = message["user"]
    message = "Hello %s!" % user
    send_message(user, message)

#route for adding a watch-phrase
@app.route('/add_phrase', methods=['POST'])
def add_phrase():
  return Response('You added a phrase!')

@app.route('/', methods=['GET'])
def test():
  return Response('It works!')
