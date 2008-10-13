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
from roadmate.models.roadmateuser import RoadMateUserForm

# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class ProfilePageHandler(BaseRequestHandler):
	"""
		Profile view

			   Will be displayed in edit mode if own profile
		Page:
			/profile.html

		Get Arguments:
			user - Integer (RoadMateUser.key.id) [Required]
	"""

	def get(self):
		## --------------------------------------------------------------------
		# Retrive Session Info and Request Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		# Request Values
		target_user_id = self.get_request_parameter('user', converter=int, default=None)

		# Datastore Values
		target_user = None
		if target_user_id > 0:
			target_user = RoadMateUser.get_by_id(target_user_id)

		# --------------------------------------------------------------------
		# Validate Session and Request
		# --------------------------------------------------------------------
		if target_user is None:
			if current_user is None:
				self.redirect(users.create_login_url(self.request.url))
				return
			else:
				# if a target user has not be specified, but the user is
				# logged in, then redirect them to their profile page.
				logging.info("No target user specified. Redirecting to"\
					" current user's profile page.")

				self.redirect("/profile?user=%s" % current_user.key().id())
				return
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = super(ProfilePageHandler, self
			).generate_template_values(self.request.url)

		# because this page requires the user to be logged in, if they logout
		# we redirect them back to the home page.
		template_values['logout_url'] = users.create_logout_url('/')

		template_values['my_rides'] = list(target_user.rides)
		template_values['target_user'] = target_user #only used if not current user

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__),
			'profile.html')
		self.response.out.write(template.render(page_path, template_values))




# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/profile', ProfilePageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
