from google.appengine.ext import db

from google.appengine.ext.db import djangoforms
from django import newforms as forms

from roadmate.models.roadmateuser import RoadMateUser

class Location(db.Model):
	"""
		Location
			A named address owned by a RoadMateUser
	"""
	name = db.StringProperty()
	owner = db.ReferenceProperty(RoadMateUser, required=True) #locations have a RoadMateUser owner
	address = db.StringProperty()
	town = db.StringProperty()
	created = db.DateTimeProperty(required=True, auto_now_add=True)

	def __unicode__(self):
		"""Returns a string representation of the object."""
		return self.name

class LocationForm(djangoforms.ModelForm):
	"""
		Form for creating location
	"""

	class Meta:
		model = Location
		exclude = ['owner', 'creation_date']