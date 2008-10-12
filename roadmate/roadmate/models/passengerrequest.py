from google.appengine.ext import db

from google.appengine.ext.db import djangoforms

from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.ride import Ride

class PassengerRequest(db.Model):
	"""
		passengerRequest

		a request made by a RoadmateUser for a seat on a ride

		this will probably only be created by the handler
		of a page displaying a ride's details  the user
		clicks a link and the request is created
		refer to the create request UC if unsure

		use Seat.accept(<PassengerRequest>) to accept the request for a given seat
	"""
	owner = db.ReferenceProperty(RoadMateUser, required=True) ##roadmateUser making the request
	ride = db.ReferenceProperty(Ride, required=True, collection_name="passengerrequests")
	created = db.DateTimeProperty(required=True, auto_now_add=True)

	def __unicode__(self):
		"""Returns a string representation of the object."""
		return self.name



