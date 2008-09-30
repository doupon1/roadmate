#!/usr/bin/env python

import os
import logging


from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.handlers.baserequesthandler import BaseRequestHandler
from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.passengerrequest import PassengerRequest

from roadmate.models.ride import Ride
from roadmate.models.ride import RideOffer
from roadmate.models.seat import Seat


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
		ride_id = self.get_request_parameter('id', converter=int, default=None)
		prq_id = self.get_request_parameter('prq_id', converter=int, default=None)
		seat_id = self.get_request_parameter('seat_id', converter=int, default=None)
		action = self.get_request_parameter('action', converter=str, default=None)

		# Datastore Values
		ride = Ride.get_by_id(ride_id)

		# --------------------------------------------------------------------
		# Handle approving and removing passengers and seats
		# --------------------------------------------------------------------
		if current_user == ride.rideoffer.owner:
		   	# Approve a passenger request
			if prq_id and action == 'APRV':
				prq = PassengerRequest.get_by_id(prq_id) #only proceed if there is a valid passengerrequest
				if prq:
					empty_seat = ride.seats.filter('passenger = ', None).get() #retrieve the empty seats on this ride
					empty_seat.assign(prq) #assign the seat: this method of Seat handles setting the "assigned time"
					prq.delete() #delete the passenger request

		   	# Remove a passenger from the seat
			if seat_id and action == 'RM':
				seat = Seat.get_by_id(seat_id) #only proceed if there is a valid seat
				if seat:
					seat.passenger = None
					seat.accepted = None #disassociate the seat from the user
					seat.save()
					#TODO notify the passenger they have been removed

			# Delete a seat
			if seat_id and action == 'DEL':
				seat = Seat.get_by_id(seat_id) #only proceed if there is a valid seat
				if seat:
					seat.delete()
					#TODO if seat has passenger, notify them

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
		template_values['lat_lng_src'] = ride.rideoffer.source.get_lat_loc()
		template_values['lat_lng_des'] = ride.rideoffer.destination.get_lat_loc()
		template_values['key'] = ride.rideoffer.destination.get_googlekey()
		template_values['has_passengers'] = (ride.count_seats() - ride.count_emptyseats()) >0

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

		# --------------------------------------------------------------------
		# Control the display of the form element
		# and handle the new request
		# --------------------------------------------------------------------

		#if user has already placed a request on this ride ~~appears in get and post
		if ride.passengerrequests.filter('owner = ', current_user).get():
			template_values['requestable'] = False #turn off the request button
		else:
			template_values['requestable'] = True #turn on the request button

			#if user is placing a request
			if self.request.POST['do_request_ride']:
				prq = PassengerRequest(owner=current_user, ride=ride) #create a new passengerrequest
				prq.put()
				template_values['requestable'] = False #turn off the request button
				self.request.POST['do_request_ride'] = False #in case of refresh/repost

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "ride_view.html")
		self.response.out.write(template.render(page_path, template_values))



# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/ride', ViewRidePageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
