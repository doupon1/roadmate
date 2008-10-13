from datetime import date

from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from django import newforms as forms
from django.newforms.util import ErrorList

from roadmate.google.googlemaps import GoogleMaps

from roadmate.models.location import Location
from roadmate.models.roadmateuser import RoadMateUser

from roadmate.widgets.selectdatewidget import SelectDateWidget
from roadmate.widgets.selecttimewidget import SelectTimeWidget

class RideRequest(db.Model):
	"""
		A request for a ride.
		These objects are publicly viewable so that potential drivers can assess the demand for offering a ride.
		In this way, it will encourage them to offer a ride they might otherwise not.

	"""

	owner = db.ReferenceProperty(RoadMateUser, collection_name="riderequests", required=True)
	source = db.ReferenceProperty(Location, verbose_name="From", collection_name="riderequests_from", required=True) ##where the owner wants the ride to begin
	destination = db.ReferenceProperty(Location, verbose_name="To", collection_name="riderequests_to", required=True) ##where the owner wants the ride to end
	date = db.DateProperty(verbose_name="Date") ##date they want the ride for
	departure_time = db.TimeProperty(verbose_name="Departure time") ##time they would like to depart
	arrival_time = db.TimeProperty(verbose_name="Arrival time") ##time they would like to arrive
	notes = db.TextProperty(verbose_name="Notes")##any comments the owner wants to make about the request
	created = db.DateTimeProperty(required=True, auto_now_add=True) ##date/time the request was created

	# get_name
	# use this method to define a standard
	# fornat of displaying the reference to a riderequest
	def get_name(self):
		return self.source.get_addressname() + " <img border='0' alt='to' src='/images/arrow.gif'/> " + self.destination.get_addressname()

 	def __unicode__(self):
		"""Returns a string representation of the object."""
		return self.get_name()


class RideRequestForm(djangoforms.ModelForm):
	"""
		Form to create a RideRequest

	"""

	# ------------------------------------------------------------------------
	#  Set the widgets we want for these attributes of RideRequest
	# ------------------------------------------------------------------------
	date = forms.DateField(widget=SelectDateWidget) #TODO set defaults/initialization on these, they are null otherwise
	departure_time = forms.TimeField(widget=SelectTimeWidget)
	arrival_time = forms.TimeField(widget=SelectTimeWidget)

	source_address = forms.CharField(label="From address", required=False)
	destination_address = forms.CharField(label="To address", required=False)

	## these clean_.. methods are all the same as Ride

	def clean_notes(self):
		notes = self.clean_data['notes']
		return notes

	def clean_date(self):
		departure_date = self.clean_data['date']

		# only allow rides in the future
		if departure_date < date.today():
			raise forms.ValidationError("Depature date cannot be in the past.")

		return departure_date

	def clean_source_address(self):
		source_address = self.clean_data['source_address']

		if not GoogleMaps.is_valid_address(source_address):
			raise forms.ValidationError("Please enter a valid address.")

		return source_address

	def get_source(self):
		source_address = self.clean_data['source_address']

		if GoogleMaps.is_valid_address(source_address):
			return Location.get_by_address(source_address, create=True)
		else:
			return None

	def clean_destination_address(self):
		destination_address = self.clean_data['destination_address']

		if not GoogleMaps.is_valid_address(destination_address):
			raise forms.ValidationError("Please enter a valid address.")

		return destination_address

	def get_destination(self):
		destination_address = self.clean_data['destination_address']

		if GoogleMaps.is_valid_address(destination_address):
			return Location.get_by_address(destination_address, create=True)
		else:
			return None

	def clean(self):
		cleaned_data = self.clean_data

		owner = cleaned_data['owner'] = self.initial['owner']

		cleaned_data['source'] = self.get_source()
		cleaned_data['destination'] = self.get_destination()

		errors = ErrorList()

		# validate times
		if cleaned_data['departure_time'] >= cleaned_data['arrival_time']:
			errors.append("Depature time must be before arrival time.")

		if errors:
			raise forms.ValidationError(errors)

		return cleaned_data

	class Meta:
		  model = RideRequest
		  exclude = ['owner', 'created', 'source', 'destination']


