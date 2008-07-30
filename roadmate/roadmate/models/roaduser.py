

from google.appengine.ext import db

class RoadUser(db.Model):
	"""
		RoadMate Data Model
		
		RoadUser
			Stores data about a site user.
	"""
	user = db.UserProperty(required=True)
	rating = db.RatingProperty(required=True, default=50)