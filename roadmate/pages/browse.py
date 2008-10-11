#!/usr/bin/env python

import os
import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.handlers.baserequesthandler import BaseRequestHandler

from roadmate.models.ride import Ride
from roadmate.models.riderequest import RideRequest
from roadmate.models.seat import Seat
from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.location import Location


# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class BrowseRidePageHandler(BaseRequestHandler):
	"""
		Controls the display of Rides as a list for browsing

		Page:
			"browse_rides.html"
		Get Arguments:
			maxresults - Integer [Default=20]
	"""

	def get(self):
		## --------------------------------------------------------------------
		# Retrive Session Info and Request Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		# Request Values
		max_results = self.get_request_parameter('maxresults', converter=int, default=20)

		# Get Datastore Values
		rides = Ride.all() #TODO this will need to be > now(), i.e. only future instances

		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = super(BrowseRidePageHandler, self
			).generate_template_values(self.request.url)

		template_values['rides'] = list(rides)
		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "browse_rides.html")
		self.response.out.write(template.render(page_path, template_values))



class BrowseRideRequestPageHandler(BaseRequestHandler):
	"""
		Controls the display of RideRequests as a list for browsing

		Page:
			"browse_riderequests.html"
		Get Arguments:
			maxresults - Integer [Default=20]
	"""

	def get(self):
		## --------------------------------------------------------------------
		# Retrive Session Info and Request Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		# Request Values
		max_results = self.get_request_parameter('maxresults', converter=int, default=20)

		# Get Datastore Values
		riderequests = RideRequest.all() #TODO this will need to be > now(), i.e. only future instances

		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = super(BrowseRideRequestPageHandler, self
			).generate_template_values(self.request.url)

		template_values['riderequests'] = list(riderequests)
		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "browse_riderequests.html")
		self.response.out.write(template.render(page_path, template_values))



# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/browse_rides', BrowseRidePageHandler),
		 ('/browse_riderequests', BrowseRideRequestPageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()

