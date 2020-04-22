import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack import WebClient
from slack.errors import SlackApiError

BOT_TOKEN = os.environ.get('BOT_TOKEN')
client = WebClient(BOT_TOKEN)

def list_channels():
  channels_call = client.conversations_list()
  if channels_call.get('ok'):
    return channels_call['channels']
  return None

def channel_info(channel_id):
  channel_info = client.conversations_info(channel=channel_id)
  if channel_info:
    return channel_info['channel']
  return None

def send_message(channel_id, message):
  try:
    response = client.chat_postMessage(
      channel=channel_id,
      text=message
    )
    print(response)
  except SlackApiError as e:
    assert e.response["error"]

if __name__ == '__main__':
  channels = list_channels()
  if channels:
    print("Channels: ")
    for channel in channels:
      if channel['name'] == 'general':
        print(channel['name'])
        print(channel['id'])
        send_message(channel['id'], "Hi, I am Bot")
      print('-------')
  else:
    print("Unable to authenticate.")
