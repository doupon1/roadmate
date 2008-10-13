#!/usr/bin/env python
# encoding: utf-8

import os
import urllib
import logging

import simplejson

from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.handlers.baserequesthandler import BaseRequestHandler

from roadmate.models.location import Location

# ----------------------------------------------------------------------------
#  Constants
# ----------------------------------------------------------------------------
WISES_FETCH_URL = "http://www.wises.co.nz/address_proxy.php"

# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class LocationCompleterRequestHandler(BaseRequestHandler):
	"""Provides auto-complete functionality for address fields.

		Page:
			/locations

		Get Arguments:
			current_value - String [Required]
	"""
	def post(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and GET Data
		# --------------------------------------------------------------------
		# Request Values
		current_value = self.get_request_parameter('current_value', converter=str, default=None)

		# --------------------------------------------------------------------
		# Validate Request
		# --------------------------------------------------------------------
		if current_value is None:
			self.error(400)
			return
			
		# strip any numbers from the front of the test

		# --------------------------------------------------------------------
		# Generate and Store Template Values
		# --------------------------------------------------------------------
		template_values = super(LocationCompleterRequestHandler, self
			).generate_template_values(self.request.url)
		
		
		fetch_url = WISES_FETCH_URL + '?address=' + urllib.quote_plus(current_value) 
		
		content = urlfetch.fetch(fetch_url).content
		query_content = simplejson.loads(content)
		
		closest_locations = []
		
		if "results" in query_content:
			results = query_content['results']
			closest_locations = map(lambda x: x['full_address'], results)
		
		template_values['closest_locations'] = closest_locations

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "location-completer.html")
		self.response.out.write(template.render(page_path, template_values))


# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web application
	application = webapp.WSGIApplication(
		[
			('/ajax/location-completer', LocationCompleterRequestHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
	main()
