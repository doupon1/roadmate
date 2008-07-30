

from google.appengine.ext import db

class Town(db.Model):
	"""
		RoadMate Data Model
		
		Town
			Stores data about a town.
	"""
	name = db.StringProperty(required=True)