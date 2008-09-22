#!/usr/bin/env python

import os
import logging
import urllib

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
		key = "ABQIAAAALCi9t1naIjEhwoF3_R48QxQtrj2yXU7uUDf9MLK2OBnE3PD31hRS8GRlNBL8LAzbUwLiBPN_wWqmoQ" 


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
		def get_lat_long(location): # This method returns a string that contains (Latitude,Longitude)   
                    output = "csv"
                    location = urllib.quote_plus(location)
                    url = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, output, key)
                    result = urlfetch.fetch(url).content
                    dlist = result.split(',')
                    if dlist[0] == '200':
                        return "%s, %s" % (dlist[2], dlist[3])
                    else:
                        return ''

		template_values = super(ViewRidePageHandler, self
			).generate_template_values(self.request.url)

		template_values['ride'] = ride
		template_values['lat_lng_src'] = get_lat_long(ride.rideoffer.source.address + ride.rideoffer.source.town)
                template_values['lat_lng_des'] = get_lat_long(ride.rideoffer.destination.address + ride.rideoffer.destination.town)
                template_values['keys'] = key
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
		#print(self.request.POST['do_request_ride'])
		# --------------------------------------------------------------------
		# Retrive POST Data
		# If the request ride bit is set, create a new request
		# --------------------------------------------------------------------
		if self.request.POST['do_request_ride']:
			prq = PassengerRequest(owner=current_user, ride=ride) #create a new passengerrequest
			prq.put()
			template_values['requested'] = True #so form can display a response



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
