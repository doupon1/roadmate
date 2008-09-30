

from google.appengine.ext import db
from google.appengine.ext.webapp import template

from google.appengine.ext.db import djangoforms
from django import newforms as forms
from django.newforms.util import ErrorList

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
	owner = db.ReferenceProperty(RoadMateUser, collection_name="rideoffers", required=True)
	source = db.ReferenceProperty(Location, collection_name="rideoffers_from", required=True)
	destination = db.ReferenceProperty(Location, collection_name="rideoffers_to", required=True)
	notes = db.TextProperty()
	creation_date = db.DateTimeProperty(auto_now_add=True, required=True)



class RideOfferForm(djangoforms.ModelForm):
	"""
		Form to create a ride offer.
	"""
    
	# ------------------------------------------------------------------------
	#  Additional value for first Ride to be created with this RideOffer
	# ------------------------------------------------------------------------
	date = forms.DateField(widget=SelectDateWidget); #TODO set defaults/initialization on these, they are null otherwise
	departure_time = forms.TimeField(widget=SelectTimeWidget);
	arrival_time = forms.TimeField(widget=SelectTimeWidget);
	number_of_seats = forms.IntegerField(initial=1);
	
	# ------------------------------------------------------------------------
	#  Alternative text fields for source and destination
	# ------------------------------------------------------------------------
	source_address = forms.CharField(label="From address", required=False)
	destination_address = forms.CharField(label="To address", required=False)
	
	# ------------------------------------------------------------------------
	#  Override display widgets
	# ------------------------------------------------------------------------
	source = djangoforms.ModelChoiceField(Location, label="From location", required=False)
	destination = djangoforms.ModelChoiceField(Location, label="To location", required=False)
	
	def clean_number_of_seats(self):
		number_of_seats = self.clean_data['number_of_seats']
		
		#TODO: this shouldn't be hardcoded
		if number_of_seats < 1:
			raise forms.ValidationError("Number of seats must be atleast one.")
		if number_of_seats > 80:
			raise forms.ValidationError("Number of seats cannot be more than 80.")
			
		return number_of_seats
	
	def clean(self):
		cleaned_data = self.clean_data
		
		owner = cleaned_data['owner'] = self.initial['owner']
		errors = ErrorList()
		#TODO: check owner exits
		
		# the user is not picking a location from their favourites, 
		# then use the 'source_address' to create a new location.
		if cleaned_data['source'] is None:
			if cleaned_data['source_address'] == "":
				errors.append("Please choose a source address.")
			else:
				source_location = Location(
					owner=owner,
					address=cleaned_data['source_address']
				)
				source_location.put()
				cleaned_data['source'] = source_location
		
		# the user is not picking a location from their favourites, 
		# then use the 'destination_address' to create a new location.
		if cleaned_data['destination'] is None:
			if cleaned_data['destination_address'] == "":
				errors.append("Please choose a destination address.")
			else:
				destination_location = Location(
					owner=owner,
					address=cleaned_data['destination_address']
				)
				destination_location.put()
				cleaned_data['destination'] = destination_location
			
		# validate times
		if cleaned_data['departure_time'] >= cleaned_data['arrival_time']:
			errors.append("Depature time must be before arrival time.")
			
		if errors:
			raise forms.ValidationError(errors)
		
		return cleaned_data
		

	class Meta:
		  model = RideOffer
		  exclude = ['owner', 'creation_date']

