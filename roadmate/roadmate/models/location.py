import urllib

from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.ext.db import djangoforms

from django import newforms as forms

from roadmate.google.googlemaps import GoogleMaps
from roadmate.models.roadmateuser import RoadMateUser

class Location(db.Model):
	"""A named address owned by a RoadMateUser."""
	name = db.StringProperty()
	owner = db.ReferenceProperty(RoadMateUser, collection_name="locations", required=True)
	address = db.StringProperty()
	created = db.DateTimeProperty(required=True, auto_now_add=True)

	def get_addressname(self):
		"""Returns the address in a human friendly form.
		"""
		if self.name is not None:
		   return self.name
		else:
			return self.address

	def get_lat_loc(self):
		"""Returns a string that contains the latitude and longitude of the
		location.
		"""
		return GoogleMaps.get_lat_loc(self.address)

	def __unicode__(self):
		"""Returns a string representation of the object."""
		return self.get_addressname()


class LocationForm(djangoforms.ModelForm):
	"""Form for creating a location."""
	class Meta:
		model = Location
		exclude = ['owner', 'creation_date']
