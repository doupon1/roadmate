#!/usr/bin/env python

import os
import logging

from google.appengine.api import users

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.handlers.baserequesthandler import BaseRequestHandler
from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.rideoffer import RideOffer
from roadmate.models.rideoffer import RideOfferForm
from roadmate.models.town import Town
# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------


		
	
	
class Cal_loginHandler(BaseRequestHandler):		
	
	def get(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and GET Data
		# --------------------------------------------------------------------
		# Session Values
		
		#template_values = self.generate_template_values(self.request.url)
		
		current_user = RoadMateUser.get_current_user()
		
		# Request Values
		rideoffer_id = self.get_request_parameter('id', converter=int, default=None)
		
		# Datastore Values
		rideoffer = RideOffer.get_by_id(rideoffer_id)
		rides = rideoffer.rides
		# --------------------------------------------------------------------
		# Validate Request
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to the home page.
		if rideoffer is None:
			self.error(404)
			return
		
		# --------------------------------------------------------------------
		# Generate and Store Template Values
		# --------------------------------------------------------------------
		template_values = super(Cal_loginHandler, self
			).generate_template_values(self.request.url)
		
		template_values['rideoffer'] = rideoffer

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		
		page_path = os.path.join(os.path.dirname(__file__), 'cal_Auth.html')
		self.response.out.write(template.render(page_path, template_values))


# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------
		

def main():
	
	# Instalise web application
	application = webapp.WSGIApplication(
		[
		 ('/cal_Authlogin', Cal_loginHandler )
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()

