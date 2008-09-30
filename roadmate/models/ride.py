from google.appengine.ext import db
from google.appengine.ext.webapp import template

from roadmate.models.rideoffer import RideOffer

class Ride(db.Model):
	"""
		Ride
			An instance of a ride. This will be created directly by the RideOffer entity
			and instances may be created periodically (for recurring rides)
			(i.e. every Wednesday, or weekdays, etc)

			Use Ride.rideoffer to get the parent object
			Use Ride.seats to get the collection of child Seats

	"""
	rideoffer = db.ReferenceProperty(RideOffer, collection_name="rides") ##parent rideoffer
	date = db.DateProperty(verbose_name="Date") ##date of this ride
	departure_time = db.TimeProperty(verbose_name="Departs") ##time of this ride departure
	arrival_time = db.TimeProperty(verbose_name="Arrives") ##date of this ride
	notes = db.TextProperty(verbose_name="Notes")
	created = db.DateTimeProperty(required=True, auto_now_add=True) ##date this ride was created

	# return the number of seats
	def count_seats(self):
		return self.seats.count()

	# return the number of unassigned seats
	def count_emptyseats(self):
		return self.seats.filter('passenger = ', None).count()

	# create_seats
	# method to create a number_of_seats
	# can only be invoked after the Ride has been saved
	def create_seats(self, number_of_seats):
		from roadmate.models.seat import Seat
		for i in range(0,number_of_seats):
			s = Seat(ride=self)
			s.put()
		return




	def __unicode__(self):
		"""Returns a string representation of the object."""
		return self.name