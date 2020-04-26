import os
from airtable import Airtable

# Airtable automatically authenticated when you have AIRTABLE_API_KEY set in env
airtable_client = Airtable(os.environ['BASE_KEY'], 'watch_phrases')

# get all phrases
def fetch_phrases():
  phrases = []
  for page in airtable_client.get_iter():
    for record in page:
      fields = record.get('fields', None)
      if fields:
        phrases.append(fields['phrase']) 
      else:
        pass   
  return phrases

# add phrase
def add_phrase(phrase):
  # ensure it's a string
  if type(phrase) is str:
    airtable_client.insert({'phrase': phrase})
  else:
    return "That doesn't look like a phrase..."

# delete phrase
def delete_phrase(phrase):
  if phrase in fetch_phrases():
    airtable_client.delete_by_field('phrase', phrase)
  else:
    return "You were never tracking that phrase..."