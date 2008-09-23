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
	owner = db.ReferenceProperty(RoadMateUser, collection_name="locations", required=True) #locations have a RoadMateUser owner
	address = db.StringProperty(required=True)
	town = db.StringProperty()
	creation_date = db.DateTimeProperty(required=True, auto_now_add=True)

	def __unicode__(self):
		"""Returns a string representation of the object."""
		
		# ideally we'd like to use the location's friendly name, if this
		# isn't available then we fallback to the location's address.
		if self.name is not None:
			return self.name
		else:
			return self.address

class LocationForm(djangoforms.ModelForm):
	"""
		Form for creating location
	"""

	class Meta:
		model = Location
		exclude = ['owner', 'creation_date']