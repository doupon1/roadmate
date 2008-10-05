#!/usr/bin/env python

import os
import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.converters import is_true
from roadmate.handlers.baserequesthandler import BaseRequestHandler
from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.ride import Ride
from roadmate.models.seat import Seat

# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class MybookingsPageHandler(BaseRequestHandler):
	"""
	   A user can view the rides on which they have booked seats.

	   Prototype 3: Adapted from the Prototype 2 profile page

	   TODO display with "cancel" functionality

		Page:
			/mybookings.html
	"""

	def get(self):
		## --------------------------------------------------------------------
		# Retrive Session Info and Request Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = super(MybookingsPageHandler, self
			).generate_template_values(self.request.url)

		# because this page requires the user to be logged in, if they logout
		# we redirect them back to the home page.
		template_values['logout_url'] = users.create_logout_url('/')

		template_values['my_booked_seats'] = list(current_user.myseats)

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__),
			'mybookings.html')

		self.response.out.write(template.render(page_path, template_values))

# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/mybookings', MybookingsPageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
