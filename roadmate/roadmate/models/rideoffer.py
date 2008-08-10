

from google.appengine.ext import db
from google.appengine.ext.webapp import template

from google.appengine.ext.db import djangoforms

from google.appengine.ext.db import datetime

from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.town import Town



class RideOffer(db.Model):
	"""
		RoadMate Data Model
		
		RideOffer
			Stores data on an offered ride.
	"""
	owner = db.ReferenceProperty(RoadMateUser, required=True)
	source = db.ReferenceProperty(Town, required=True,
		collection_name='outgoing_rides', default=Town.all().get())
	destination = db.ReferenceProperty(Town, required=True,
		collection_name='incomming_rides', default=Town.all().get())
	date = db.DateProperty()
	time = db.TimeProperty()
	available_seats = db.IntegerProperty(required=True, default=1)
	notes = db.TextProperty()
	creation_date = db.DateTimeProperty(required=True, auto_now_add=True)
	
class RideOfferForm(djangoforms.ModelForm):
	"""
		RoadMate Django ModelForm

		RoadUserForm
			Form for ride offers.
	"""
	class Meta:
		model = RideOffer
		exclude = ['owner', 'creation_date']

class RideOfferSearch(db.Model):
	"""
		RoadMate Data Model

		RideOfferSearch
			Stores search data for ride offer.
	"""
	source = db.StringProperty(choices=[town.name for town in Town.all()])
	destination = db.StringProperty(choices=[town.name for town in Town.all()])

class RideOfferSearchForm(djangoforms.ModelForm):
	"""
		RoadMate Django ModelForm

		RideOfferSearchForm
			Form for searching for ride offers.
	"""
	class Meta:
		model = RideOfferSearch
					