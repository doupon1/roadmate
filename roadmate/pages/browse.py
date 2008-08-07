#!/usr/bin/env python

import os
import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.handlers.baserequesthandler import BaseRequestHandler
from roadmate.models.rideoffer import RideOffer
from roadmate.models.rideoffer import RideOfferSearch
from roadmate.models.rideoffer import RideOfferSearchForm
from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.town import Town

# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class BrowseRideOffersPageHandler(BaseRequestHandler):
	"""
		RoadMate RequestHandler
		
		Page:
			/browse.html
		Get Arguments:
			source - String
			destination - String
			maxresults - Integer [Default=20]
	"""	
		
	def get(self):
		## --------------------------------------------------------------------
		# Retrive Session Info and Request Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()
		
		# Request Values
		source = self.get_request_parameter('source', default=None)
		destination = self.get_request_parameter('destination', default=None)
		max_results = self.get_request_parameter('maxresults', converter=int, default=20)
		
		# Datastore Values
		rides = db.GqlQuery("SELECT * FROM RideOffer"\
							" WHERE source = :source"\
							"  AND destination = :destination"\
							" ORDER BY date, time"\
						 	" LIMIT %u" % max_results,
			source=Town.all().filter("name =", source).get(),
			destination=Town.all().filter("name =", destination).get()
		)
		
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = super(BrowseRideOffersPageHandler, self
			).generate_template_values(self.request.url)
		
		ride_search = RideOfferSearch(source=source, destination=destination)
		template_values['search_form'] = RideOfferSearchForm(instance=ride_search)
		template_values['rides'] = list(rides)
		
		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "browse_rideoffers.html")			
		self.response.out.write(template.render(page_path, template_values))
		

# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Instalise web application
	application = webapp.WSGIApplication(
		[
		 ('/browse', BrowseRideOffersPageHandler)
		], debug=True)
	run_wsgi_app(application)

# ----------------------------------------------------------------------------
#  Load Custom Django Template Filters
# ----------------------------------------------------------------------------
webapp.template.register_template_library('roadmate.filters')
	
if __name__ == '__main__':
  main()
