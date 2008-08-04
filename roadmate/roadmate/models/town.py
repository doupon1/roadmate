

from google.appengine.ext import db

class Town(db.Model):
	"""
		RoadMate Data Model
		
		Town
			Stores data about a town.
	"""
	name = db.StringProperty(required=True)
	geo_location = db.GeoPtProperty()
	
	def __unicode__(self):
		"""Returns a string representation of the object."""
		return self.name
	