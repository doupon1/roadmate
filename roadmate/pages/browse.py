#!/usr/bin/env python

import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.handlers.baserequesthandler import BaseRequestHandler
from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.roadmateuser import RoadMateUserForm

# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class BrowseRideOffersPageHandler(BaseRequestHandler):
	"""
		RoadMate RequestHandler
		
		Page:
			/profile.html
		Get Arguments:
			user - Integer (RoadMateUser.key.id) [Required]
			edit - Boolean [Default=False]
			
	"""	
		
	def get(self):
		# --------------------------------------------------------------------
		# Retrive and Validate Request
		# --------------------------------------------------------------------
		# Default Values
		current_user = RoadMateUser.get_current_user()
		target_user = None
		is_editing = False
		
		# Retrive 'user' parameter
		try:
			target_user_id = int(self.request.get('user'))
			target_user = RoadMateUser.get_by_id(target_user_id)		
			
		except (TypeError, ValueError), e:
			logging.info("No target user specified.")
			
		# Retrive 'edit' paramater
		if self.request.get('edit') is not None:
			is_editing = (self.request.get('edit') == "True")
		
		# Validate request
		if target_user is None:
			if current_user is None:
				self.redirect(users.create_login_url(self.request.url))
				return
			else:
				# if a target user has not be specified but the user is logged
				# in, then redirect to their profile page.
				logging.info("No target user specified. Redirecting to"\
					" current user's profile page.")
				self.redirect("/profile?user=%s&edit=%s" % 
					(current_user.key().id(), is_editing))
				return
		
		# Validate request
		if is_editing:
			if target_user != current_user:
				# if the user is trying to edit someone elses profile page,
				# redirect them to the read-only version.
				if current_user is None:
					logging.warning("A guest attempted to view the edit"\
						" profile page of user '%s'. Redirecting to read-only"\
						" version." % target_user.user.email)
				else:
					logging.warning("User '%s' attempted to view the edit"\
						" profile page of user '%s'. Redirecting to read-only"\
						" version." % 
						(current_user.user.email, target_user.user.email))
					
				self.redirect("/profile?user=%s" % target_user.key().id())
				return
		
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = super(ProfilePageHandler, self
			).generate_template_values(self.request.url)
			
		# because this page requires the user to be logged in, if they logout
		# we redirect them back to the home page.
		template_values['logout_url'] = users.create_logout_url('/')
		
		template_values['target_user'] = target_user
		template_values['user_form'] = RoadMateUserForm(instance=target_user)
		
		# --------------------------------------------------------------------
		# Render and Server Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__),
			'profile_view.html')
		
		if is_editing:
			page_path = os.path.join(os.path.dirname(__file__),
				'profile_edit.html')
			
		self.response.out.write(template.render(page_path, template_values))
		
	def post(self):
		# --------------------------------------------------------------------
		# Retrive and Validate Request
		# --------------------------------------------------------------------
		# Default Values
		current_user = RoadMateUser.get_current_user()
		target_user = None
		
		# Retrive POST parameters
		try:
			target_user_id = int(self.request.get('_id'))
			target_user = RoadMateUser.get_by_id(target_user_id)		
			
		except (TypeError, ValueError), e:
			logging.error("Invalid POST parameter: %s."\
				" Redirecting to error page." % e)
			
			# if the POST request is missing the target user id, then return
			# an error page. (400: Bad Request).
			self.error(400)
			return
		
		if target_user != current_user:
			# if the user is trying to edit someone elses profile page,
			# then present them with an error page (403: Forbidden).
			logging.error("User '%s' attempted to modify the profile of"\
				" user '%s'. Redirecting to error page." %
				(current_user.user.email, target_user.user.email))
				
			self.error(403)
			return
		
		user_form = RoadMateUserForm(data=self.request.POST,
			instance=target_user)
		
		if user_form.is_valid():
			user_form.save()
			self.redirect('/profile')
			return
		
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = BaseRequestHandler.generate_template_values(self,
			self.request.url)

		# because this page requires the user to be logged in, if they logout
		# we redirect them back to the home page.
		template_values['logout_url'] = users.create_logout_url('/')

		template_values['target_user'] = target_user
		template_values['user_form'] = user_form

		# --------------------------------------------------------------------
		# Render and Server Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), 'profile_edit.html')
		self.response.out.write(template.render(page_path, template_values))

# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Instalise web application
	application = webapp.WSGIApplication(
		[
		 ('/browse', ProfilePageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
