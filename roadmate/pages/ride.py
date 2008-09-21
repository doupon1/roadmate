#!/usr/bin/env python

import os
import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.handlers.baserequesthandler import BaseRequestHandler
from roadmate.models.roadmateuser import RoadMateUser

from roadmate.models.ride import Ride


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

	def get(self):
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
