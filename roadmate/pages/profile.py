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
		template_values['user_form'] = RoadMateUserForm(instance=current_user) #only used if current user

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__),
			'profile.html')

		self.response.out.write(template.render(page_path, template_values))

	def post(self):
		# --------------------------------------------------------------------
		# Retrive and Validate Request
		# --------------------------------------------------------------------
		# Default Values
		current_user = RoadMateUser.get_current_user()

		# --------------------------------------------------------------------
		# Validate Sesson
		# --------------------------------------------------------------------
		# if the current users in not logged in, then we redirect them through
		# a login page.
		if current_user is None:
			self.redirect(users.create_login_url(self.request.url))
			return

		target_user = None

		# --------------------------------------------------------------------
		# Retrive POST Data
		# --------------------------------------------------------------------
		# POST Values
		target_user_id = self.get_request_parameter('_id', converter=int, default=None)
		target_user = RoadMateUser.get_by_id(target_user_id)

		# --------------------------------------------------------------------
		# Validate POST Data
		# --------------------------------------------------------------------
		# if the target user does not exist in the datastore, then redirect
		# the user back to an error page.
		if target_user is None:
			self.error(404)
			return

		# if the user is trying to edit someone elses profile page,
		# then present them with an error page (403: Forbidden).
		if target_user != current_user:
			logging.error("User '%s' attempted to modify the profile of"\
				" user '%s'. Redirecting to error page." %
				(current_user.user.email, target_user.user.email))

			self.error(403)
			return

		user_form = RoadMateUserForm(data=self.request.POST,
			instance=target_user)

		# if there are errors in the form, then re-serve the page with the
		# error values highlighted.
		if not user_form.is_valid():
			# ----------------------------------------------------------------
			# Generate Template Values
			# ----------------------------------------------------------------
			template_values = super(ProfilePageHandler, self
				).generate_template_values(self.request.url)

			# because this page requires the user to be logged in, if they
			# logout we redirect them back to the home page.
			template_values['logout_url'] = users.create_logout_url("/")

			template_values['target_user'] = target_user
			template_values['user_form'] = user_form

			# ----------------------------------------------------------------
			# Render and Serve Template
			# ----------------------------------------------------------------
			page_path = os.path.join(os.path.dirname(__file__), "profile.html")
			self.response.out.write(template.render(page_path, template_values))
			return

		# --------------------------------------------------------------------
		# Finalise POST Request
		# --------------------------------------------------------------------
		user_form.save()
		self.redirect("/profile?user=%s" % current_user.key().id())

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
