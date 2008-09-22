
from google.appengine.ext import db

from google.appengine.ext.webapp import template

from google.appengine.ext.db import djangoforms
from django import newforms as forms


from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.location import Location


from roadmate.widgets.selectdatewidget import SelectDateWidget
from roadmate.widgets.selecttimewidget import SelectTimeWidget

class RideOffer(db.Model):
	"""
		RideOffer
            An offer of some rides from one location to another.

			Use RideOffer.rides to get the collection of child Rides
	"""
	owner = db.ReferenceProperty(RoadMateUser, required=True)
	source = db.ReferenceProperty(Location, verbose_name="From", collection_name="rideoffers_from", default=Location.all().get()) #TODO only Owned locations should show
	destination = db.ReferenceProperty(Location, verbose_name="To", collection_name="rideoffers_to", default=Location.all().get())
	notes = db.TextProperty(verbose_name="Notes")
	created = db.DateTimeProperty(required=True, auto_now_add=True)



class RideOfferForm(djangoforms.ModelForm):
	"""
		Form to create a ride offer.
	"""
    #form variables for setting up the (at first, single) Ride belonging to this RideOFfer
	date = forms.DateField(label="Date", widget=SelectDateWidget); #TODO set defaults/initialization on these, they are null otherwise
	departure_time = forms.TimeField(label="Departure Time", widget=SelectTimeWidget);
	arrival_time = forms.TimeField(label="Arrival Time", widget=SelectTimeWidget);
	number_of_seats = forms.IntegerField(label="Number of Seats", initial=1);

	class Meta:
		  model = RideOffer
		  exclude = ['owner', 'creation_date']

