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

class ProfilePageHandler(BaseRequestHandler):
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
		
		# Retrive GET parameters
		try:
			target_user_id = int(self.request.get('user'))
			target_user = RoadMateUser.get_by_id(target_user_id)		
			is_editing = (self.request.get('edit') == "True")
			
		except (TypeError, ValueError):
			logging.error('invalid GET parameters')
		
		# Validate setttings
		if target_user is None:
			if current_user is None:
				self.redirect(users.create_login_url(self.request.url))
			else:
				# if a target user has not be specified but the user is logged
				# in, then redirect to their profile page.
				self.redirect('/profile?user=%s&edit=%s' % 
					(current_user.key().id(), is_editing))
		
		if is_editing:
			if target_user != current_user:
				# if the user is trying to edit someone elses profile page,
				# redirect them to the read-only version.
				self.redirect('/profile?user=%s' % current_user.key().id())
		
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = BaseRequestHandler.generate_template_values(self,
			self.request.url)
			
		# because this page requires the user to be logged in, if they logout
		# we redirect them back to the home page.
		template_values['logout_url'] = users.create_logout_url('/')
		
		template_values['target_user'] = target_user
		template_values['user_form'] = RoadMateUserForm(instance=target_user)
		
		# --------------------------------------------------------------------
		# Render and Server Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), 'profile_view.html')
		
		if is_editing:
			page_path = os.path.join(os.path.dirname(__file__), 'profile_edit.html')
			
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
			
		except (TypeError, ValueError), (strerror):
			logging.error('Invalid POST parameters: %s' % strerror)
			
			# if the POST request is missing the target user id, then return
			# an error page. (400: Bad Request).
			self.error(400)
			return
		
		if target_user != current_user:
			# if the user is trying to edit someone elses profile page,
			# then present them with an error page (403: Forbidden).
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
		 ('/profile', ProfilePageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
