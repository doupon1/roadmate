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

class RideOfferPageHandler(BaseRequestHandler):
	"""
		RoadMate RequestHandler
		
		Page:
			/ride/offer
		Get Arguments:
			id - Integer (RideOffer.key.id) [Required]
			edit - Boolean [Default=False]
			
	"""	
		
	def get(self):
		# --------------------------------------------------------------------
		# Retrive and Validate Request
		# --------------------------------------------------------------------
		# Default Values
		current_user = RoadMateUser.get_current_user()
		target_ride = None
		is_editing = False
		
		# Retrive GET parameters
		try:
			target_ride_id = int(self.request.get('id'))
			target_ride = RideOffer.get_by_id(target_ride_id)		
			is_editing = (self.request.get('edit') == "True")
			
		except (TypeError, ValueError):
			logging.error('invalid GET parameters')
		
		# if the target ride does not exist in the datastore, then redirect
		# the user back to the home page.
		if target_ride is None:
			self.redirect('/')
			# TODO: This should display an error page
		
		if is_editing:
			if target_ride.owner != current_user:
				# if the user is trying to edit a ride they did not create,
				# redirect them to the read-only version.
				self.redirect('/rideoffer?id=%s' % target_ride.key().id())
		
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = BaseRequestHandler.generate_template_values(self,
			self.request.url)
			
		# because this page requires the user to be logged in, if they logout
		# we redirect them back to the home page.
		if is_editing:
			template_values['logout_url'] = users.create_logout_url('/')
		
		template_values['target_ride'] = target_ride
		template_values['ride_form'] = RideOfferForm(instance=target_ride)
		
		# --------------------------------------------------------------------
		# Render and Server Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), 'rideoffer_view.html')
		
		if is_editing:
			page_path = os.path.join(os.path.dirname(__file__), 'rideoffer_edit.html')
			
		self.response.out.write(template.render(page_path, template_values))


class CreateRideOfferPageHandler(BaseRequestHandler):
	"""
		RoadMate RequestHandler
		
		Page:
			/ride/offer/create
			
	"""	
		
	def get(self):
		# --------------------------------------------------------------------
		# Retrive and Validate Request
		# --------------------------------------------------------------------
		# Default Values
		current_user = RoadMateUser.get_current_user()
		
		# if the current users in not logged in, then we redirect them through
		# a login page.
		if current_user is None:
			self.redirect(users.create_login_url(self.request.url))
			return
		
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = BaseRequestHandler.generate_template_values(self,
			self.request.url)
			
		# because this page requires the user to be logged in, if they logout
		# we redirect them back to the home page.
		template_values['logout_url'] = users.create_logout_url('/')
		
		
		ride_offer = RideOffer(owner=current_user)
		template_values['ride_form'] = RideOfferForm(instance=ride_offer)
		
		# --------------------------------------------------------------------
		# Render and Server Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), 'rideoffer_create.html')			
		self.response.out.write(template.render(page_path, template_values))
	
	def post(self):
		# --------------------------------------------------------------------
		# Retrive and Validate Request
		# --------------------------------------------------------------------
		# Default Values
		current_user = RoadMateUser.get_current_user()

		# if the current users in not logged in, then we redirect them through
		# a login page.
		if current_user is None:
			self.redirect(users.create_login_url(self.request.url))
			return

		ride_offer = RideOffer(owner=current_user)
		ride_form = RideOfferForm(data=self.request.POST,
			instance=ride_offer)

		if ride_form.is_valid():
			ride_form.save()
			self.redirect('/rideoffer?id=%s' % ride_form.instance.key().id())
			return

		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = BaseRequestHandler.generate_template_values(self,
			self.request.url)

		# because this page requires the user to be logged in, if they logout
		# we redirect them back to the home page.
		template_values['logout_url'] = users.create_logout_url('/')

		template_values['ride_form'] = ride_form

		# --------------------------------------------------------------------
		# Render and Server Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), 'rideoffer_create.html')
		self.response.out.write(template.render(page_path, template_values))


# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	
	# Instalise web application
	application = webapp.WSGIApplication(
		[
		 ('/rideoffer_create', CreateRideOfferPageHandler),
		 ('/rideoffer', RideOfferPageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
