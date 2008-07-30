

from google.appengine.ext import db

from roadmate.models.roaduser import RoadUser
from roadmate.models.town import Town

class Ride(db.Model):
	"""
		RoadMate Data Model
		
		Ride
			Stores data on an offered ride.
	"""
	owner = db.ReferenceProperty(RoadUser, required=True)
	source = db.ReferenceProperty(Town, required=True,
		collection_name='ride_source_set')
	destination = db.ReferenceProperty(Town, required=True,
		collection_name='ride_desination_set')
	datetime = db.DateTimeProperty(required=True)
	seats = db.IntegerProperty(required=True)
	notes = db.TextProperty()