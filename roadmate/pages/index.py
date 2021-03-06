#!/usr/bin/env python
import os
import datetime

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
		OneDay = datetime.timedelta(days=1)
		Yesterday = datetime.datetime.now() - OneDay

		rides = db.GqlQuery("SELECT * FROM Ride \
							WHERE date > :1 \
							ORDER BY date, created DESC LIMIT 10", 
							Yesterday)

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


if __name__ == '__main__':
  main()
