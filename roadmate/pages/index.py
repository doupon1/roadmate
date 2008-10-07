#!/usr/bin/env python
import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.handlers.baserequesthandler import BaseRequestHandler
from roadmate.models.ride import Ride


# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class IndexPageHandler(BaseRequestHandler):
	"""
		RoadMate RequestHandler

		Pages:
			/index.html
	"""

	def generate_template_values(self, page_path):
		"""
			generate_template_values

			Generates a dictionary of template values required by the pages
			served from this request handler.

		"""


		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = BaseRequestHandler.generate_template_values(self,
			page_path)

		#10 most recently created rides

		rides = db.GqlQuery("SELECT * FROM Ride ORDER BY creation_date DESC LIMIT 10")

		# --------------------------------------------------------------------
		# Store Template Values
		# --------------------------------------------------------------------

		template_values['rides'] = list(rides)

		return template_values


	def get(self):
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = self.generate_template_values(self.request.url)

		template_values['logout_url'] = users.create_logout_url('/')

		# --------------------------------------------------------------------
		# Render and Server Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(page_path, template_values))

# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():

	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/', IndexPageHandler),
		 ('/index.html', IndexPageHandler)
		], debug=True)
	run_wsgi_app(application)

# ----------------------------------------------------------------------------
#  Load Custom Django Template Filters
# ----------------------------------------------------------------------------
webapp.template.register_template_library('roadmate.filters')

if __name__ == '__main__':
  main()
