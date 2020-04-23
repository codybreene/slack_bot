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
    os.environ['SLACK_SIGNING_SECRET'], endpoint='/events', server=app)
client = WebClient(os.environ['BOT_TOKEN'])

watch_phrases = []

def send_message(id, message):
  try:
    response = client.chat_postMessage(
      channel=id,
      text=message
    )
  except SlackApiError as e:
    assert e.response['error']

def check_inclusion(message, watch_phrases):
  for phrase in watch_phrases:
    if message in watch_phrases:
      return message 
    else:
      continue 
  return None

@events_adapter.on('message')
def handle_message(event_data):
  message = event_data['event']
  if 'yolo' in message.get('text'):
    print(message)
    user = message['user']
    message = f"Hi! You're receiving this message because you mentioned " 
    send_message(user, message)

#route for adding a watch-phrase
@app.route('/add_phrase', methods=['POST'])
def add_phrase():
  phrase = request.form.get('text')
  if phrase not in watch_phrases:
    watch_phrases.append(phrase)
    return Response(f'You added a phrase: {phrase} All phrases: {watch_phrases}')
  else:
    return Response('You already added that phrase')

#route for deleting a watch-phrase
@app.route('/delete_phrase', methods=['POST'])
def delete_phrase():
  phrase = request.form.get('text')
  if phrase in watch_phrases:
    watch_phrases.remove(phrase)
    return Response(f'You deleted a phrase: {phrase} All phrases: {watch_phrases}')
  else:
    return Response("That's not a watch-phrase")

@app.route('/', methods=['GET'])
def test():
  return Response('It works!')
