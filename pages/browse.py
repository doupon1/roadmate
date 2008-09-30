#!/usr/bin/env python

import os
import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.handlers.baserequesthandler import BaseRequestHandler

from roadmate.models.rideoffer import RideOffer
from roadmate.models.ride import Ride
from roadmate.models.seat import Seat
from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.location import Location

# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class BrowseRidePageHandler(BaseRequestHandler):
	"""
		Page for handling the display of Rides for browsing

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
		rides = Ride.all()

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


# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/browse', BrowseRidePageHandler)
		], debug=True)
	run_wsgi_app(application)

# ----------------------------------------------------------------------------
#  Load Custom Django Template Filters
# ----------------------------------------------------------------------------
webapp.template.register_template_library('roadmate.filters')

if __name__ == '__main__':
  main()
