import urllib

from google.appengine.ext import db
from google.appengine.api import urlfetch
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
	address = db.StringProperty()
	town = db.StringProperty()
	created = db.DateTimeProperty(required=True, auto_now_add=True)

	# get_addressname
	# this is the way the address will be referenced in "plain text" on the site
	# since some addresses are not named, can return the address for these
	def get_addressname(self):
		if self.name is not None:
		   return self.name
		else:
			return self.address

	# get_googlekey
	# The url key needed for the google map
	def get_googlekey(self):
		return "ABQIAAAALCi9t1naIjEhwoF3_R48QxQtrj2yXU7uUDf9MLK2OBnE3PD31hRS8GRlNBL8LAzbUwLiBPN_wWqmoQ"


	# get_lat_long method
	# Returns a string that contains (Latitude,Longitude)
	# TODO verify it is working (moved it here offline and changed it without testing)
	def get_lat_loc(self):
		try:
			output = "csv"
			location = urllib.quote_plus(self.address)
			url = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, output, self.get_googlekey())
			result = urlfetch.fetch(url).content
			dlist = result.split(',')
			if dlist[0] == '200':
				return "%s, %s" % (dlist[2], dlist[3])
			else:
			   	return ''
		except Exception:
			return ''

	def __unicode__(self):
		"""Returns a string representation of the object."""
		return self.get_addressname()



class LocationForm(djangoforms.ModelForm):
	"""
		Form for creating location
	"""

	class Meta:
		model = Location
		exclude = ['owner', 'creation_date']
