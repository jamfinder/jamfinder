#models
from sqlalchemy import (Table, Column, Integer, String,
                        DateTime, Float, ForeignKey)
import config

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(30), unique=True)
    jambase_artist_id = db.Column(Integer, unique=True)
    sc_user_id = db.Column(String(30), unique=True)
    url = db.Column(String(30), unique=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __init__(self, jambase_artist_id, name, url, sc_artist_id = None):
        self.sc_user_id = sc_artist_id
        self.name = name
        self.url = url
        self.jambase_artist_id


    def __repr__(self):
        return "[Artist: %s %s %s]" % (self.sc_user_id, self.name, self.url)

class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(Integer, primary_key=True)
    jambase_venue_id = db.Column(Integer, unique=True)
    name = db.Column(String(30), unique=False)
    city = db.Column(String(30), unique=False)
    address = db.Column(String(50), unique=False)
    state = db.Column(String(50), unique=False)
    zipcode = db.Column(Integer, unique=False)
    lat = db.Column(Float, unique=False)
    lng = db.Column(Float, unique=False)

    def __init__(self, jambase_venue_id, name, lat, lng,
                 city, address, state, zipcode):
        self.jambase_venue_id = jambase_venue_id
        self.name = name
        self.lat = lat
        self.lng = lng
        self.city = city
        self.zipcode = zipcode
        self.address = address
        self.state = state

    def __repr__(self):
        return "[venue: %s %s %s %s]" %(self.name, self.city, self.zipcode, self.state)

class Track:
    __tablename__ = 'track'
    id = db.Column(Integer, primary_key=True)
    sc_track_id = db.Column(String(30), unique=True)
    sc_user_id = db.Column(String(30), unique=True)
    purchase_url = db.Column(String(120))
    artwork_url = db.Column(String(120))
    genre = db.Column(String(50))

    def __init__(self, sc_track_id, user_id, purchase_url, artwork_url, genre):
        self.sc_track_id = sc_track_id
        self.user_id = user_id
        self.purchase_url = purchase_url
        self.artwork_url = artwork_url
        self.genre = genre

    def __repr__(self):
        return "%s %s %s %s %s" % (self.sc_track_id_id, self.user_id, self.purchase_url,
                                   self.artwork_url, self.genre)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(Integer, primary_key=True)
    event_id = db.Column(Integer, primary_key=True)
    artists = db.relationship('Artist', backref='event.id',
                                lazy='dynamic')
    event_date = db.Column(DateTime, unique=False)
    venue_id = Column(Integer, ForeignKey('venue.id'))
    venue = db.relationship("Venue")
    event_url = db.Column(String)
    zipcode = db.Column(Integer)

    def __init__(self, event_id, artists, event_date, venue, event_url):
        self.event_id = event_id
        self.artists = artists
        self.event_date = event_date
        self.venue = venue
        self.event_url = event_url

    def __repr__(self):
        return "%s %s %s %s %s" % (self.event_id, str(self.artists), self.event_date,
                                   self.venue, self.event_url)

class PrevRequest(db.Model):
    __tablename__ = 'prev_request'
    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(Integer, unique=True)
    radius = db.Column(Integer, unique=True)
    date = db.Column(DateTime)

    def __init__(self, zipcode, radius, date):
        self.zipcode = zipcode
        self.radius = radius
        self.date = date

    def __repr__(self):
        return "%s %s %s" % (self.zipcode, self.radius, self.date)
