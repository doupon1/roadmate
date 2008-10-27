

from google.appengine.ext import db
from google.appengine.ext.webapp import template

from google.appengine.ext.db import djangoforms
from django import newforms as forms

from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.ride import Ride
from roadmate.models.passengerrequest import PassengerRequest

class Seat(db.Model):
	"""
		Seat
			A ride has instances of this class associated with it to
			represent the physical seats which will be assigned to passengers

			Seats won't usually be created directly, they should be constructed
			by the owning Ride (probably on its own construction)

			Maybe there should be methods on the seat for the passenger (once assigned)
			to be able to contact the ride owner, and vice versa?

		Usage notes:
			Use seat.passenger to determine whether it is assigned
			Use seat.accept() to accept a passengerRequest, don't set passenger publicly

	"""
	ride = db.ReferenceProperty(Ride, collection_name="seats") ##parent ride
	passenger = db.ReferenceProperty(RoadMateUser, collection_name="myseats") ##the lucky passenger who has been assigned to this seat
	accepted = db.DateTimeProperty() ##the day/time when the seat's passenger was set

	# assign
	# To assign a PassengerRequest to this seat
	def assign(self, passenger_request):
		self.passenger = passenger_request.owner
		self.accepted = db.DateTimeProperty.now()
		self.save()
		return

	# unicode descripter
	def __unicode__(self):
		"""Returns a string representation of the object."""
		return self.name
