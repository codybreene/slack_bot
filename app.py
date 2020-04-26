import os
import logging
logging.basicConfig(level=logging.DEBUG)

from flask import Flask, request, Response
from slack import WebClient
from slack.errors import SlackApiError
from slackeventsapi import SlackEventAdapter
from airtable_util import fetch_phrases, create_record, delete_record

#instantiate app
app = Flask(__name__)

events_adapter = SlackEventAdapter(
    os.environ['SLACK_SIGNING_SECRET'], endpoint='/events', server=app)
client = WebClient(os.environ['BOT_TOKEN'])

def send_message(id, message):
  try:
    response = client.chat_postMessage(
      channel=id,
      blocks=message
    )
  except SlackApiError as e:
    assert e.response['error']

def check_inclusion(message):
  watch_phrases = fetch_phrases()
  print(watch_phrases)
  print(message)
  for phrase in watch_phrases:
    if phrase in message:
      print(phrase)
      return phrase
    else:
      continue 
  return None

@events_adapter.on('message')
def handle_message(event_data):
  message = event_data['event']
  trigger_phrase = check_inclusion(message['text'])
  print(trigger_phrase)
  if trigger_phrase:
    user = message['user']
    #format reply in a slack block
    reply = [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Hi there! We're messaging you because your recent message contained the following trigger phrase: *{trigger_phrase}*"
        }
    }]
    send_message(user, reply)
  else:
    pass

#slash command route for adding a watch-phrase
@app.route('/add_phrase', methods=['POST'])
def add_phrase():
  phrase = request.form.get('text')
  watch_phrases = fetch_phrases()
  if phrase not in watch_phrases:
    create_record(phrase)
    return Response(f'You added a watch-phrase: {phrase}')
  else:
    return Response('You already added that phrase')

#slash command route for deleting a watch-phrase
@app.route('/delete_phrase', methods=['POST'])
def delete_phrase():
  phrase = request.form.get('text')
  watch_phrases = fetch_phrases()
  if phrase in watch_phrases:
    delete_record(phrase)
    return Response(f'You deleted a phrase: {phrase}')
  else:
    return Response("That's not a watch-phrase")

@app.route('/', methods=['GET'])
def test():
  return Response('App is running -- test out the functionality within Slack!')

  
