import urllib

from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.ext.db import djangoforms
from django.template.defaultfilters import escape
from django import newforms as forms

from django.template.defaultfilters import escape
from roadmate.google.googlemaps import GoogleMaps
from roadmate.models.roadmateuser import RoadMateUser

class Location(db.Model):
	"""A named address owned by a RoadMateUser."""
	address = db.StringProperty(required=True)
	geo_point = db.GeoPtProperty(required=True)
	creation_date = db.DateTimeProperty(required=True, auto_now_add=True)

	def get_addressname(self):
		"""Returns the address in a human friendly form.
		"""
		return escape(self.address)

	def get_lat_loc(self):
		"""Returns a string that contains the latitude and longitude of the
		location.
		"""
		return "%f, %f" % (self.geo_point.lat, self.geo_point.lon)

	def __unicode__(self):
		"""Returns a string representation of the object."""
		return self.get_addressname()

	@staticmethod
	def get_by_address(address, create):
		location = Location.all().filter('address=', address).get()

		# add the location to the database if it dosen't already exist
		if location is None and create:
			location = Location(
				address = address,
				geo_point = GoogleMaps.get_geo_point(address)
			)
		location.put()

		return location
