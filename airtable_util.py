import os
from airtable import Airtable
from keys import AIRTABLE_API_KEY, AIRTABLE_BASE_KEY

#Airtable is auto authenticated when you have AIRTABLE_API_KEY set in env
airtable_client = Airtable(AIRTABLE_BASE_KEY, 'watch_phrases', api_key=AIRTABLE_API_KEY)

#get all phrases
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

#add phrase
def create_record(phrase):
  # ensure it's a string
  if type(phrase) is str:
    airtable_client.insert({'phrase': phrase})
  else:
    return "That doesn't look like a phrase..."

#delete phrase
def delete_record(phrase):
  if phrase in fetch_phrases():
    airtable_client.delete_by_field('phrase', phrase)
  else:
    return "You were never tracking that phrase..."