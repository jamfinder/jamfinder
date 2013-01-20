#models
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float
import config

# DB class
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  config.DB_URI
db = SQLAlchemy(app)

class Venue(db.Model):
    __tablename__ = 'venue'
     id = db.Column('id', Integer, primary_key=True)
     name = db.Column('name', String(30), unique=True)
     city = db.Column('city', String(30), unique=False)
     address = db.Column('address', String(50), unique=False)
     state = db.Column('state', String(50), unique=False)
     zipcode = db.Column('zipcode', Integer, unique=False)

     def __init__(self, name, city, address, state):
         self.name = name
         self.city = city
         self.zipcode = zipcode
         self.address = address
         self.state = state

    def __repr__(self):
      return "[venue: %s %s %s %s]" %(self.name, self.city, self.zipcode, self.state)

class Event(db.Model):
    __tablename__ = 'event'

    event_id = db.Column('event_id', Integer, primary_key=True)
    artists

    def __init__(self, event_id, artists, event_date, venue, event_url):
        self.event_id = event_id
        self.artists = artists
        self.event_date = event_date
        self.venue = venue
        self.event_url = event_url

  def __repr__(self):
      return "%s %s %s %s %s" % (self.event_id, self.artists, self.event_date,
                                 self.venue, self.event_url)
