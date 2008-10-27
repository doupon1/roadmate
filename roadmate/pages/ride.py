#!/usr/bin/env  python


import os
import logging

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.converters import is_true
from roadmate.google.googlemaps import GoogleMaps
from roadmate.google.googlecalendar import GoogleCalendar
from roadmate.handlers.baserequesthandler import BaseRequestHandler

from roadmate.filters import time_for_table

from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.passengerrequest import PassengerRequest
from roadmate.models.ride import Ride
from roadmate.models.ride import RideForm
from roadmate.models.seat import Seat
from roadmate.models.location import Location
from roadmate.models.message import RideMessage
from roadmate.models.riderequest import RideRequest
# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class ViewRidePageHandler(BaseRequestHandler):
	"""
		RoadMate RequestHandler

		Page:
			/ride ( = ride_view.html)

		Get Arguments:
			id - Integer (Ride.key.id) [Required]
	"""
#GET REQUEST HANDLER
	def get(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and GET Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		# Request Values
		ride_id = self.get_request_parameter('id', converter=int, default=-1) # ride
		prq_id = self.get_request_parameter('prq_id', converter=int, default=None) # passenger request (accept)
		action = self.get_request_parameter('action', converter=str, default=None)
		seat_id = self.get_request_parameter('seat_id', converter=int, default=None) # seat (remove passenger)

		# Datastore Values
		ride = Ride.get_by_id(ride_id)

		# --------------------------------------------------------------------
		# Validate Request
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to the home page.
		if ride is None:
			self.error(404)
			return

		# --------------------------------------------------------------------
		# Handle approving and removing passengers and seats
		# --------------------------------------------------------------------
		if current_user == ride.owner:
		   	# Approve a passenger request
			if prq_id and action == 'APRV':
				prq = PassengerRequest.get_by_id(prq_id) #only proceed if there is a valid passengerrequest
				if prq and (ride.count_emptyseats() > 0):
					empty_seat = ride.seats.filter('passenger = ', None).get() #retrieve the empty seats on this ride
					empty_seat.assign(prq) #assign the seat: this method of Seat handles setting the "assigned time"
					prq.delete() #delete the passenger request
					# notify the approved passenger
					mail.send_mail(sender="massey.group.356@gmail.com",
		              to=prq.owner.user.email(),
		              subject="RoadMate - Your passenger request has been approved",
		              body=generate_approvepassenger_email_body(ride))

		   	# Remove a passenger from the seat
			if seat_id and action == 'RM':
				seat = Seat.get_by_id(seat_id) #only proceed if there is a valid seat
				if seat:
					# notify the removed passenger
					mail.send_mail(sender="massey.group.356@gmail.com",
		              to=seat.passenger.user.email(),
		              subject="RoadMate - Removed from ride",
		              body=generate_removedpassenger_email_body(ride))
					#disassociate the seat from the user
					seat.passenger = None
					seat.accepted = None
					seat.save()



		# --------------------------------------------------------------------
		# Generate and Store Template Values
		# --------------------------------------------------------------------
		template_values = super(ViewRidePageHandler, self
			).generate_template_values(self.request.url)

		template_values['ride'] = ride
		template_values['lat_lng_src'] = ride.source.get_lat_loc()
		template_values['lat_lng_des'] = ride.destination.get_lat_loc()
		template_values['googlemaps_key'] = GoogleMaps.get_key()
		template_values['google_calendar_key'] = GoogleCalendar.get_key()
		template_values['has_passengers'] = (ride.count_seats() - ride.count_emptyseats()) > 0 # has some passengers
		template_values['message_list'] = list(ride.ridemessages.order('created')) # the list of comments
		template_values['has_occurred'] =  False #(ride.date < ride.date.today()) # is in the past
		template_values['is_full'] = (ride.count_emptyseats() == 0) # no empty seats
		template_values['enable_feedback_on_driver'] =  template_values['has_occurred'] & ride.is_passenger(current_user) # ride is in the past and current user has been passenger
		template_values['enable_feedback_on_passengers'] = template_values['has_occurred'] & (current_user == ride.owner) # ride is in the past and current user was owner
		template_values['enable_edit_controls'] = (not template_values['has_occurred']) & (current_user == ride.owner) # ride is in the future and current user is owner
		template_values['enable_passenger_withdraw'] = (not template_values['has_occurred']) & ride.is_passenger(current_user) # ride is in the future and current user is passenger

		# --------------------------------------------------------------------
		# Control the display of the form element
		# --------------------------------------------------------------------
		#if user has already placed a request on this ride ~~appears in get and post
		if ride.passengerrequests.filter('owner = ', current_user).get():
			template_values['requestable'] = False #turn off the request button
		else:
			template_values['requestable'] = True #turn on the request button



		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "ride_view.html")
		self.response.out.write(template.render(page_path, template_values))



#POST REQUEST HANDLER
	def post(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and GET Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		if current_user is None:
			self.redirect(users.create_login_url(self.request.url))
			return


		# Request Values
		ride_id = self.get_request_parameter('id', converter=int, default=None)

		# Datastore Values
		ride = Ride.get_by_id(ride_id)
		# --------------------------------------------------------------------
		# Validate Request
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to the home page.
		if ride is None:
			self.error(404)
			return


		# --------------------------------------------------------------------
		# Generate and Store Template Values
		# --------------------------------------------------------------------
		template_values = super(ViewRidePageHandler, self
			).generate_template_values(self.request.url)

		template_values['ride'] = ride
		template_values['lat_lng_src'] = ride.source.get_lat_loc()
		template_values['lat_lng_des'] = ride.destination.get_lat_loc()
		template_values['googlemaps_key'] = GoogleMaps.get_key()
		template_values['google_calendar_key'] = GoogleCalendar.get_key()
		template_values['has_passengers'] = (ride.count_seats() - ride.count_emptyseats()) > 0 # has some passengers
		template_values['message_list'] = list(ride.ridemessages.order('created')) # the list of comments
		template_values['has_occurred'] =  False #(ride.date < ride.date.today()) # is in the past
		template_values['is_full'] = (ride.count_emptyseats() == 0) # no empty seats
		template_values['enable_feedback_on_driver'] =  template_values['has_occurred'] & ride.is_passenger(current_user) # ride is in the past and current user has been passenger
		template_values['enable_feedback_on_passengers'] = template_values['has_occurred'] & (current_user == ride.owner) # ride is in the past and current user was owner
		template_values['enable_edit_controls'] = (not template_values['has_occurred']) & (current_user == ride.owner) # ride is in the future and current user is owner
		template_values['enable_passenger_withdraw'] = (not template_values['has_occurred']) & ride.is_passenger(current_user) # ride is in the future and current user is passenger


		# --------------------------------------------------------------------
		# Control the display of the form element
		# and handle the new request
		# --------------------------------------------------------------------

		# if user is cancelling their ride
		if current_user == ride.owner and self.request.POST.has_key('do_cancel_ride'):
			#TODO notify all the passengers!
			ride.delete()
			self.redirect("/") # redirect to the main page
			return


		# if passenger is withdrawing
		if ride.is_passenger(current_user) and self.request.POST.has_key('do_withdraw'):
			passenger_seat = ride.seats.filter('passenger = ', user).get() # find the passenger's seat
			self.redirect("/ride?id=%s" % ride.key().id()) # redirect back to the view page
			# notify the driver
			mail.send_mail(sender="support@roadmate.com",
		              to=ride.owner.user.email(),
		              subject="RoadMate - Passenger has withdrawn",
		              body=generate_withdrawpassenger_email_body(ride))
			#disassociate the seat from the user
			passenger_seat.passenger = None
			passenger_seat.accepted = None
			passenger_seat.save()

			return

		#if user has already placed a request on this ride ~~appears in get and post
		if ride.passengerrequests.filter('owner = ', current_user).get():
			template_values['requestable'] = False #turn off the request button
		else:
			template_values['requestable'] = True #turn on the request button


		#if user is placing a passenger request
		if self.request.POST.has_key('do_request_ride') and self.request.POST['do_request_ride']:
			prq = PassengerRequest(owner=current_user, ride=ride) #create a new passenger request
			prq.put()
			template_values['requestable'] = False #turn off the request button


		#if user is posting a message
		#TODO make this more secure! clean the title and body text and validate max/min length!

		if self.request.POST.has_key('do_post_message') and self.request.POST['do_post_message']:
			message = RideMessage(author=current_user, ride=ride, title=self.request.POST['message_title'], text=self.request.POST['message_body'])
			message.put()

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "ride_view.html")
		self.response.out.write(template.render(page_path, template_values))








class CreateRidePageHandler(BaseRequestHandler):
	"""
		Create Ride view

		 For Prototype 3, creation of Rides is handled here
		 instead of creating the Ride when the (now deprecated) RideOffer is created
		 the Route is created (or a previously-created Route is reused)
		 at the time the Ride is created

		Page:
			/ride_create

		Get Arguments:
			showSourceFavorites - Boolean [Default=False]
			showDestinationFavorites - Boolean [Default=False] TODO fix these to also show favorite Routes
	"""

#GET REQUEST HANDLER
	def get(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and Request Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		# --------------------------------------------------------------------
		# Validate Session and Request
		# --------------------------------------------------------------------
		# if the current users in not logged in, then we redirect them through
		# a login page.
		if current_user is None:
			self.redirect(users.create_login_url(self.request.url))
			return

		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = super(CreateRidePageHandler, self
			).generate_template_values(self.request.url)

		# because this page requires the user to be logged in, if they logout
		# we redirect them back to the home page.
		template_values['logout_url'] = users.create_logout_url("/")
		template_values['owner'] = current_user

		template_values['ride_form'] = RideForm()

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "ride_create.html")
		self.response.out.write(template.render(page_path, template_values))

#POST REQUEST HANDLER
	def post(self):
		# --------------------------------------------------------------------
		# Retrive Session Info
		# --------------------------------------------------------------------
		# Session Values
		rq_id = self.get_request_parameter('rq', converter=int, default=None) #if created with a ride request
		current_user = RoadMateUser.get_current_user()

		# --------------------------------------------------------------------
		# Validate Sesson
		# --------------------------------------------------------------------
		# if the current users in not logged in, then we redirect them through
		# a login page.
		if current_user is None:
			self.redirect(users.create_login_url(self.request.url))
			return

		# --------------------------------------------------------------------
		# Retrive POST Data
		# i.e. form has been submitted, do sth with the values
		# --------------------------------------------------------------------

		ride_data = { 'owner':current_user }

		ride_form = RideForm(
			data=self.request.POST,
			initial=ride_data
		) #set a form for that instance

		# --------------------------------------------------------------------
		# Validate POST Data
		# --------------------------------------------------------------------
		# if there are errors in the form, then re-serve the page with the
		# error values highlighted.
		if not ride_form.is_valid():
			# ----------------------------------------------------------------
			# Generate Template Values
			# ----------------------------------------------------------------
			template_values = BaseRequestHandler.generate_template_values(self,
				self.request.url)


			# because this page requires the user to be logged in, if they
			# logout we redirect them back to the home page.
			template_values['logout_url'] = users.create_logout_url("/")
			template_values['owner'] = current_user

			template_values['ride_form'] = ride_form

			# ----------------------------------------------------------------
			# Render and Serve Template
			# ----------------------------------------------------------------
			page_path = os.path.join(os.path.dirname(__file__), "ride_create.html")
			self.response.out.write(template.render(page_path, template_values))
			return

		ride = ride_form.save() #else, the form is valid, so save it
		if rq_id:
			request = RideRequest.get_by_id(rq_id)
			print(request.owner.user.email) #TODO notify him by email that a ride has been created

		ride.create_seats(ride_form.clean_data.get('number_of_seats')) # create its seats

		#notification if created by ride request
		if rq_id:
			request = RideRequest.get_by_id(rq_id)
			print(request.owner.user.email) #TODO notify him by email that a ride has been created and send the link

		self.redirect("/ride?id=%s" % ride.key().id()) # redirect to the view page

# functions to generate the body text for email notifications
# this is removed from the rest of the class because the """ statements require absolute indenting
# so putting these here make the code more legible
	def generate_removedpassenger_email_body(ride):
		return """
This is to notify you that you have been removed as a passenger from the ride """ + ride.get_name + """

Although you had been approved as a passenger on this ride, the driver
has chosen to remove you. This is the driver's decision as it is their
own responsibility to decide who will travel with them in their car.

Thanks,

The RoadMate team
"""

	def generate_withdrawpassenger_email_body(ride):
		return """
This is to notify you that a passenger has withdrawn from your ride, """ + ride.get_name + """

If you want, you can assign their seat to another user,
via the Manage My Rides page.

Thanks,

The RoadMate team.
"""

	def generate_approvepassenger_email_body(ride):
		return """
This is to notify you that your request for a seat on the ride """ + ride.get_name + """ has been approved.

You can now view the details of this ride under Manage My Bookings. If your plans change,
or you cannot make it to the ride, please use the Withdraw function to let the driver know you aren't coming
so they can give the seat to someone else.

Thanks,

The RoadMate team.
"""


# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/ride', ViewRidePageHandler),
		 ('/ride_create', CreateRidePageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
