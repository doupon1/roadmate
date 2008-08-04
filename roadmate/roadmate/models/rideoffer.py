

from google.appengine.ext import db
from google.appengine.ext.webapp import template

from google.appengine.ext.db import djangoforms

from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.town import Town

class RideOffer(db.Model):
	"""
		RoadMate Data Model
		
		Ride
			Stores data on an offered ride.
	"""
	owner = db.ReferenceProperty(RoadMateUser, required=True)
	source = db.ReferenceProperty(Town, required=True,
		collection_name='ride_source_set', default=Town.all().get())
	destination = db.ReferenceProperty(Town, required=True,
		collection_name='ride_desination_set', default=Town.all().get())
	date = db.DateProperty(required=True, auto_now_add=True)
	time = db.TimeProperty()
	available_seats = db.IntegerProperty(required=True, default=1)
	notes = db.TextProperty()
	creation_date = db.DateTimeProperty(required=True, auto_now_add=True)
	
class RideOfferForm(djangoforms.ModelForm):
	"""
		RoadMate Django ModelForm

		RoadUserForm
			Form for RideOffer.
	"""
	class Meta:
		model = RideOffer
		exclude = ['owner', 'creation_date']