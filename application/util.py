import json
import logging
import datetime, time
import models
import utils
import settings
import urllib
import soundcloud

def open_remote_api(query, api):
  """
  Calls a remote API with a query. Returns json.
  Google App Enging sometimes fails to open the URL properly resulting in a DownloadError.
  So we have to do it more often sometimes ...
  """
  if api == "googlemaps":
      api_url = settings_private.GOOGLE_MAPS_API_URL
      api_name = "Google Maps API"
  if api == "jambase":
      api_url = settings_private.JAMBASE_API_KEY
      api_name = 'Jambase API'
  query = api_url + query
  logging.info("Requesting %s with uri: %s" % (api_name, query))
  i = 0
  while True:
    if (i >= settings.API_RETRIES):
      break
    try:
      result = urlfetch.fetch(query, deadline=10) # raises DownloadError sometimes
      i = 0
      break
    except DownloadError:
      pass
    i += 1

  if i != 0:
    logging.error("Connection to %s failed." % api_name)
    raise DownloadError("Connection to %s failed." % api_name)
  logging.info("Result for %s Query: %s" % (api_name, result.content))
  return json.loads(result.content)

def get_users(client, name):
    artist = client.get('/users', q=name)
    exact_artist = filter(lambda x: x.full_name.lower == name.lower)
    if len(artist)  == 0:
        exact_artist = artist
        return map (operator.attrgetter('id'), exact_artist)

def get_latest_song_from_user(user_id, time_from=None, time_to=None):
    if not time_from: time_from = calculate_time_from()
    if not time_to: time_to = datetime.datetime.now().isoformat()
    return tracks

genres = {}
genres.update({'house': ['house', 'tech house', 'deep house', 'progressive house', 'tech-house',
                         'electro house', 'techhouse', 'minimal house', 'minimal-house',
                         'funky house', 'dance']})
genres.update({'techno': ['techno', 'techno minimal', 'minimal techno', 'minimal-techno']})
genres.update({'dubstep': ['dubstep', 'dub step']})
genres.update({'hiphop': ['hip hop', 'hip-hop', 'hiphop', 'rap', 'r&b', 'rnb', 'r\'n\'b']})
genres.update({'electronic': ['electronic', 'electro', 'electronica', 'minimal', 'idm']})
genres.update({'drumandbass': ['drum & bass', 'drum and bass', 'drum n bass', 'dnb', 'drum\'n\'bass', 'breakbeat', 'drum&bass', 'breaks']})
genres.update({'trance': ['trance', 'progressive_trance', 'progessive trance', 'psy trance', 'goa']})
genres.update({'rock': ['rock']})
genres.update({'indie': ['indie', 'alternative', 'acoustic']})
genres.update({'pop': ['pop']})
genres.update({'ambient': ['ambient']})
genres.update({'jazz': ['jazz', 'free jazz', 'nu-jazz', 'nu jazz', 'swing']})
genres.update({'classical': ['classical', 'classic']})

top_cities = ['Berlin', 'Paris', 'London', 'New York', 'Los Angeles', 'Tokyo', 'Stockholm', 'Barcelona', 'Istanbul', 'Manchester', 'Hamburg', 'Seattle', 'Miami']]})
