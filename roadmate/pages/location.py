#!/usr/bin/env python

import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.google.googlemaps import GoogleMaps
from roadmate.handlers.baserequesthandler import BaseRequestHandler

from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.location import Location

# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class ViewLocationPageHandler(BaseRequestHandler):
	"""Handles display of locations.
	
		Page:
			/location
	"""

	def get(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and GET Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		# Request Values
		target_location_id = self.get_request_parameter('id', converter=int, default=None)

		# Datastore Values
		target_location = Location.get_by_id(target_location_id)

		# --------------------------------------------------------------------
		# Validate Request
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to the home page.
		if target_location is None:
			self.error(404)
			return

		# --------------------------------------------------------------------
		# Generate and Store Template Values
		# --------------------------------------------------------------------
		template_values = super(ViewLocationPageHandler, self
			).generate_template_values(self.request.url)

		template_values['target_location'] = target_location
		template_values['googlemaps_key'] = GoogleMaps.get_key()

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "location_view.html")
		self.response.out.write(template.render(page_path, template_values))


# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/location', ViewLocationPageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
