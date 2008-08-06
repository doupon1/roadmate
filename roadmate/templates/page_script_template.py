#!/usr/bin/env python

import os
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

																				#	<==	Insert additional imports here

# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------


class PageHandler(BaseRequestHandler):											#	<==	Rename to <page name>PageHandler. ie. CreateRidePageHandler
	"""
		RoadMate RequestHandler
		
		Page:
																				#	<==	Insert names of pages served by this handler here
	"""	
		
	def get(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and Request Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()
		
		# --------------------------------------------------------------------
		# Validate Session and Request
		# --------------------------------------------------------------------
		
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = BaseRequestHandler.generate_template_values(self,
			self.request.url)
		
		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "<template file>")	#	<==	Insert template page name here		
		self.response.out.write(template.render(page_path, template_values))
	
	def post(self):
		# --------------------------------------------------------------------
		# Retrive Session Info
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		# --------------------------------------------------------------------
		# Validate Session
		# --------------------------------------------------------------------

		# --------------------------------------------------------------------
		# Retrive POST Data
		# --------------------------------------------------------------------

		# --------------------------------------------------------------------
		# Validate POST Data
		# --------------------------------------------------------------------

		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = BaseRequestHandler.generate_template_values(self,
			self.request.url)

		# --------------------------------------------------------------------
		# Finalise POST Request
		# --------------------------------------------------------------------

# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Instalise web application
	application = webapp.WSGIApplication(
		[
#		 ("/rideoffer_create", CreateRideOfferPageHandler),						#	<==	Replace these with the appropriate hander names
#		 ("/rideoffer_edit", EditRideOfferPageHandler),
#		 ('/rideoffer', ViewRideOfferPageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
