import json
import logging
import datetime, time
#import models
import utils
import settings
import urllib2, urllib
import soundcloud
import datetime
import cgi
from flask import json
from bs4 import BeautifulSoup
import jsonpickle
import operator
from fuzzywuzzy import fuzz

class Venue:
  def __init__(self, name, lat, lng, zipcode):
    self.name = name
    self.lat = lat
    self.lng = lng
    self.zipcode = zipcode

  def __repr__(self):
    return "[venue: %s %s %s %s]" %(self.name, self.lat, self.lng, self.zipcode)

class Event:
  def __init__(self, event_id, artists, event_date, venue, event_url):
    self.event_id = event_id
    self.artists = artists
    self.event_date = event_date
    self.venue = venue
    self.event_url = event_url

  def __repr__(self):
    return "%s %s %s %s %s" % (self.event_id, self.artists, self.event_date,
                               self.venue, self.event_url)

class Artist:
  def __init__(self, artist_id, name, url):
    self.artist_id = artist_id
    self.name = name
    self.url = url
  def __repr__(self):
    return "[Artist: %s %s %s]" % (self.artist_id, self.name, self.url)

class Track:
  def __init__(self, track_id, user_id, purchase_url, artwork_url, genre):
    self.track_id = track_id
    self.user_id = user_id
    self.purchase_url = purchase_url
    self.artwork_url = artwork_url
    self.genre = genre

def get_soup(url):
  try:
    req = urllib2.Request(url)
  except urllib2.HTTPError:
    pass
  return BeautifulSoup(urllib2.urlopen(req).read())

def parse_xml_response(content):
  tree = BeautifulSoup(content)
  events = []
  for event in tree('event'):
    artists = []
    for artist in event('artists'):
      artist_id = artist.find('artist_id').text
      artists.append(Artist(artist_id, artist.find('artist_name').text, None))
                            #get_official_website(artist_id)))
    venue = event.find('venue')
    venue_name = venue.find('venue_name').text
    venue_city = venue.find('venue_city').text
    venue_state = venue.find('venue_state').text
    venue_zip = venue.find('venue_zip').text
    venue_address = get_address(event.find('event_id').text)
    (lat, lng) = get_latlng(venue_address)
    venue_obj = Venue(venue_name, lat, lng, venue_zip)
    events.append(Event(event.find('event_id').text,
                        artists, event.find('event_date').text,
                          venue_obj, event.find('event_url').text))
  return events

def open_remote_api(query, api):
  """
  Calls a remote API with a query. Returns json.
  Google App Enging sometimes fails to open the URL properly resulting in a DownloadError.
  So we have to do it more often sometimes ...
  """
  if api == "googlemaps":
    api_url = settings.GOOGLE_MAPS_API_URL
    api_name = "Google Maps API"
  if api == 'geocode':
    api_url = settings.GOOGLE_GEOCODE_API_URL
    api_name = "Google Geocode API"
  if api == "jambase":
    api_url = settings.JAMBASE_API_URL
    api_name = 'Jambase API'
  query = api_url + query
  print query
  logging.info("Requesting %s with uri: %s" % (api_name, query))
  i = 0
  while True:
    if (i >= settings.API_RETRIES):
      break
    try:
      req = urllib2.Request(query)
      result = urllib2.urlopen(req).read()
      i = 0
      break
    except Exception:
      pass
    i += 1
  if i != 0:
    logging.error("Connection to %s failed." % api_name)
    raise Exception("Connection to %s failed." % api_name)
  logging.info("Result for %s Query: %s" % (api_name, result))
  if api == 'jambase':
    return parse_xml_response(result)
  else:
    return json.loads(result)
def canonical_url(u):
  u = u.lower()
  if u.startswith("http://"):
    u = u[7:]
  if u.startswith("www."):
    u = u[4:]
  if u.endswith("/"):
    u = u[:-1]
    return u

def get_official_website(jambase_artist_id):
  url = settings.JAMBASE_ARTIST_URL + 'ArtistID=%s' %jambase_artist_id
  result = get_soup(url).find_all("a", text='Official Website')
  if len(result) > 0 :
    print result[0]['href']
    return canonical_url(result[0]['href'])
  else:
    return None

def get_address(jambase_event_id):
  url = settings.JAMBASE_EVENT_URL + 'eventid=%s' %jambase_event_id
  soup = get_soup(url)
  street_address = soup.find_all("dd", class_="streetAddress")[0].contents[-1].strip()
  city_address = soup.find_all("dd", class_="cityAddress")[0].text.strip()
  address = "%s %s" %(street_address, city_address)
  return address

def get_soundcloud_id(client, artist):
  artists = client.get('/users', q=artist.name)
  print artist.name, len(artists)
  if len(artists) == 0:
    return None
  artist_fuzzs = [(x, fuzz.token_set_ratio(artist.name,
                                               x.username)) for x in artists]
  max_artist = max(artist_fuzzs, key = operator.itemgetter(1))
  if max_artist[1] > 85:
    return max_artist[0].id
  else:
    return None

def fetch_concert_info(zipcode, radius, start_date,
                       end_date, num_result):
  zipcode = "zip=%s" % zipcode if zipcode else ""
  start_date = "startDate=%s" % start_date.strftime('%m/%d/%y') if start_date else ""
  end_date = "endDate=%s" % end_date.strftime('%m/%d/%y') if end_date else ""
  radius = "radius=%s" % radius if radius else ""
  num_result = "n=%d" % num_result if num_result else ""
  params = [zipcode, start_date, end_date, radius, num_result]
  query_string  = "&".join(filter (lambda x :len(x) >0, params))
  return open_remote_api(query_string, 'jambase')

def get_artist_songs(client, artist_id):
  artist_tracks = []
  tracks = client.get('/users/%s/tracks' % artist_id)
  i = 0
  for track in tracks:
    if i == settings.MAX_SONG_NUM:
      break
    artist_tracks.append(Track(track.id, track.user_id, track.purchase_url,
                               track.artwork_url, track.genre))
  return artist_tracks

def get_songs(client, artist):
  artist_tracks = []
  tracks = client.get('/tracks', q=artist.name, order='hotness')
  i = 0
  for track in tracks:
    if i == settings.MAX_SONG_NUM:
      break
    artist_tracks.append(Track(track.id, track.user_id, track.purchase_url,
                               track.artwork_url, track.genre))
  return artist_tracks

def get_latlng(address):
  query_string='&%s' % urllib.urlencode({'address':address, 'sensor':'true'})
  response = open_remote_api(query_string, 'geocode')
  print type(response)
  loc = response[unicode('results')][0][unicode('geometry')][unicode('location')]
  return (loc[unicode('lat')], loc[unicode('lng')])

def get_concert_songs(zipcode, radius=50, start_date = datetime.date.today(),
                      end_date = None, num_result = 10):
  client = soundcloud.Client(client_id=settings.SOUNDCLOUD_CONSUMER_KEY)
  concerts = fetch_concert_info(zipcode, radius, start_date, end_date, num_result)
  print "#concerts ", len(concerts)
  concert_results = []
  for concert in concerts:
    songs = []
    for artist in concert.artists:
      soundcloud_id = get_soundcloud_id(client, artist)
      if not soundcloud_id:
        songs.extend(get_songs(client, artist))
      else:
        songs.extend(get_artist_songs(client, soundcloud_id))
    concert.songs = songs
  len(concerts)
  return jsonpickle.encode(concerts)

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

if __name__=="__main__":
  # print fetch_concert_info(19104)
  # client = soundcloud.Client(client_id=settings.SOUNDCLOUD_CONSUMER_KEY)
  # print get_users(client, '')
  # print get_location('3900 chestnut street philadelphia')
  print get_concert_songs(19104)
