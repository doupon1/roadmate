#!/usr/bin/env python

import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.handlers.baserequesthandler import BaseRequestHandler

# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class AboutPageHandler(BaseRequestHandler):
	"""
		RoadMate RequestHandler
		
		Pages:
			/about.html
	"""	
		
	def get(self):
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = self.generate_template_values(self.request.url)
		
		# --------------------------------------------------------------------
		# Render and Server Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), 'about.html')
		self.response.out.write(template.render(page_path, template_values))
		

# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	
	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/about', AboutPageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
