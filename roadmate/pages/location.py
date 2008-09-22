#!/usr/bin/env python

import os
import logging
import urllib

from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.handlers.baserequesthandler import BaseRequestHandler
from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.location import Location
from roadmate.models.location import LocationForm

# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class CreateLocationPageHandler(BaseRequestHandler):
	"""
		Handles Get and Post requests for the CreateLocation page
		Page:
			/location_create	
	"""	
	#~~~~~~~~~~~~~~~~~~~~get REQUEST~~~~~~~~~~~~~~~~~~~~
	def get(self):
		# --------------------------------------------------------------------
		# Retrieve Session Info and Request Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()
		
		# --------------------------------------------------------------------
		# Validate Session and Request
		# --------------------------------------------------------------------
		# if the current users in not logged in, then we redirect them through
		# a login page.
		if current_user is None:
			self.redirect(users.create_login_url(self.request.url))
			return
		
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = super(CreateLocationPageHandler, self	).generate_template_values(self.request.url)
			
			
		
		new_location = Location(owner=current_user) # create new location instance
		template_values['location_form'] = LocationForm(instance=new_location) #bind the form to the new location instance
			
			
		# because this page requires the user to be logged in, if they logout
		# we redirect them back to the home page.
		template_values['logout_url'] = users.create_logout_url("/")
		
		
		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "location_create.html")			
		self.response.out.write(template.render(page_path, template_values))
	
	
	#~~~~~~~~~~~~~~~~~~~~POST REQUEST~~~~~~~~~~~~~~~~~~~~
	def post(self):
		# --------------------------------------------------------------------
		# Retrive Session Info
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()
		

		# --------------------------------------------------------------------
		# Validate Sesson
		# --------------------------------------------------------------------
		# if the current users in not logged in, then we redirect them through
		# a login page.
		if current_user is None:
			self.redirect(users.create_login_url(self.request.url))
			return

		# --------------------------------------------------------------------
		# Retrive POST Data
		# --------------------------------------------------------------------
		new_location = Location(owner=current_user) # create new location instance
		location_form = LocationForm(data=self.request.POST, instance=new_location) #create the form, populate with form values
		
		


		# --------------------------------------------------------------------
		# Validate POST Data
		# --------------------------------------------------------------------
		# if there are errors in the form, then re-serve the page with the
		# error values highlighted.
		if not location_form.is_valid():
			# ----------------------------------------------------------------
			# Generate Template Values
			# ----------------------------------------------------------------

			template_values = BaseRequestHandler.generate_template_values(self,self.request.url)

			# because this page requires the user to be logged in, if they
			# logout we redirect them back to the home page.
			template_values['logout_url'] = users.create_logout_url("/")

			template_values['location_form'] = location_form

			# ----------------------------------------------------------------
			# Render and Serve Template
			# ----------------------------------------------------------------
			page_path = os.path.join(os.path.dirname(__file__), "rideoffer_create.html")
			self.response.out.write(template.render(page_path, template_values))
			return

		# --------------------------------------------------------------------
		# Finalise POST Request
		# --------------------------------------------------------------------
		location_form.save()
		self.redirect("/location?id=%s" % new_location.key().id())
 
	
class ViewLocationPageHandler(BaseRequestHandler):
	"""
		View a Location's details
		

	"""
		
	def get(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and GET Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()
		key = "ABQIAAAALCi9t1naIjEhwoF3_R48QxQtrj2yXU7uUDf9MLK2OBnE3PD31hRS8GRlNBL8LAzbUwLiBPN_wWqmoQ" 
		
		# Request Values
		target_location_id = self.get_request_parameter('id', converter=int, default=None)
		
		# Datastore Values
		target_location = Location.get_by_id(target_location_id)
		
		# --------------------------------------------------------------------
		# Validate Request
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to the home page.
		if target_location is None:
			self.error(404)
			return
		
		# --------------------------------------------------------------------
		# Generate and Store Template Values
		# --------------------------------------------------------------------
		def get_lat_long(location): # This method returns a string that contains (Latitude,Longitude)   
                        output = "csv"
                        location = urllib.quote_plus(location)
                        url = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, output, key)
                        result = urlfetch.fetch(url).content
                        dlist = result.split(',')
                        if dlist[0] == '200':
                                return "%s, %s" % (dlist[2], dlist[3])
                        else:
                                return ''
                        
		template_values = super(ViewLocationPageHandler, self
			).generate_template_values(self.request.url)
		
		template_values['target_location'] = target_location
		template_values['lat_lng_loc'] = get_lat_long(target_location.address + target_location.town)
		template_values['key'] = key
 
		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "location_view.html")
		self.response.out.write(template.render(page_path, template_values))


# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/location_create', CreateLocationPageHandler),
		 ('/location', ViewLocationPageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
