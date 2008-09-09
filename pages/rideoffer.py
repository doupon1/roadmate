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

class CreateRideOfferPageHandler(BaseRequestHandler):
	"""
		RoadMate RequestHandler
		
		Page:
			/rideoffer_create	
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
		# if the current users in not logged in, then we redirect them through
		# a login page.
		if current_user is None:
			self.redirect(users.create_login_url(self.request.url))
			return
		
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = super(CreateRideOfferPageHandler, self
			).generate_template_values(self.request.url)
			
		# because this page requires the user to be logged in, if they logout
		# we redirect them back to the home page.
		template_values['logout_url'] = users.create_logout_url("/")
		
		ride_offer = RideOffer(owner=current_user)
		template_values['ride_form'] = RideOfferForm(instance=ride_offer)
		
		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "rideoffer_create.html")			
		self.response.out.write(template.render(page_path, template_values))
	
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
		ride_offer = RideOffer(owner=current_user)
		ride_form = RideOfferForm(
			data=self.request.POST,
			instance=ride_offer
		)

		# --------------------------------------------------------------------
		# Validate POST Data
		# --------------------------------------------------------------------
		# if there are errors in the form, then re-serve the page with the
		# error values highlighted.
		if not ride_form.is_valid():
			# ----------------------------------------------------------------
			# Generate Template Values
			# ----------------------------------------------------------------
			template_values = BaseRequestHandler.generate_template_values(self,
				self.request.url)

			# because this page requires the user to be logged in, if they
			# logout we redirect them back to the home page.
			template_values['logout_url'] = users.create_logout_url("/")

			template_values['ride_form'] = ride_form

			# ----------------------------------------------------------------
			# Render and Serve Template
			# ----------------------------------------------------------------
			page_path = os.path.join(os.path.dirname(__file__), "rideoffer_create.html")
			self.response.out.write(template.render(page_path, template_values))
			return

		# --------------------------------------------------------------------
		# Finalise POST Request
		# --------------------------------------------------------------------
		ride_form.save()
		self.redirect("/rideoffer?id=%s" % ride_offer.key().id())
		
		
		
		
		
		

class EditRideOfferPageHandler(BaseRequestHandler):
	"""
		RoadMate RequestHandler
		
		Page:
			/rideoffer_edit	
		
		GET Arguments:
			id - Integer (RideOffer.key.id) [Required]
			
		POST Parameters:
			_id - Integer (RideOffer.key.id) [Required]
	"""
	def get(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and Request Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()
		
		# Request Values
		target_ride_id = self.get_request_parameter('id', converter=int, default=None)
		
		# Datastore Values
		target_ride = RideOffer.get_by_id(target_ride_id)
		
		# --------------------------------------------------------------------
		# Validate Session and Request
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to the home page.
		if target_ride is None:
			self.error(404)
			return
		
		# if the user is trying to view the edit page for a ride they did 
		# not create, then redirect them to the read-only version.
		if target_ride.owner != current_user:
			if current_user is None:
				logging.warning("A guest attempted to view the edit"\
					" ride page of user '%s'. Redirecting to read-only"\
					" version." % target_ride.owner.user.email)
			else:
				logging.warning("User '%s' attempted to view the edit"\
					" profile page of user '%s'. Redirecting to read-only"\
					" version." % 
					(current_user.user.email, target_ride.owner.user.email))
					
			self.redirect("/rideoffer?id=%s" % target_ride.key().id())
			return
		
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = super(EditRideOfferPageHandler, self
			).generate_template_values(self.request.url)
			
		# because the user is viewing the page in edit mode, then logging out
		# should redirect to the read-only version.
		template_values['logout_url'] = users.create_logout_url(
			"/rideoffer?id=%s" % target_ride.key().id())
		
		template_values['target_ride'] = target_ride
		template_values['ride_form'] = RideOfferForm(instance=target_ride)
		
		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "rideoffer_edit.html")
		self.response.out.write(template.render(page_path, template_values))
		
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
		# POST Values
		target_ride_id = self.get_request_parameter('_id', converter=int, default=None)
		target_ride = RideOffer.get_by_id(target_ride_id)
		
		# --------------------------------------------------------------------
		# Validate POST Data
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to an error page.
		if target_ride is None:
			self.error(404)
			return
		
		# if the user is trying to edit a ride they did not create,
		# redirect them to an error page (403: Forbidden).
		if target_ride.owner != current_user:
			logging.warning("User '%s' attempted to edit a ride offer"\
				" belonging to user '%s'. Redirecting to an error page."  % 
				(current_user.user.email, target_ride.owner.user.email))
			
			self.error(403)
			return
		
		ride_form = RideOfferForm(
			data=self.request.POST,
			instance=target_ride
		)
		
		# if there are errors in the form, then re-serve the page with the
		# error values highlighted.
		if not ride_form.is_valid():
			# ----------------------------------------------------------------
			# Generate Template Values
			# ----------------------------------------------------------------
			template_values = super(EditRideOfferPageHandler, self
				).generate_template_values(self.request.url)

			# because this page requires the user to be logged in, if they
			# logout we redirect them back to the home page.
			template_values['logout_url'] = users.create_logout_url("/")

			template_values['ride_form'] = ride_form

			# ----------------------------------------------------------------
			# Render and Serve Template
			# ----------------------------------------------------------------
			page_path = os.path.join(os.path.dirname(__file__), "rideoffer_edit.html")
			self.response.out.write(template.render(page_path, template_values))
			return

		# --------------------------------------------------------------------
		# Finalise POST Request
		# --------------------------------------------------------------------
		ride_form.save()
		self.redirect("/rideoffer?id=%s" % target_ride.key().id())
	
	
	
	
	
	

	
class ViewRideOfferPageHandler(BaseRequestHandler):
	"""
		RoadMate RequestHandler
		
		Page:
			/rideoffer ( = rideoffer_view.html)
		
		Get Arguments:
			id - Integer (RideOffer.key.id) [Required]
	"""
		
	def get(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and GET Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()
		
		# Request Values
		target_ride_id = self.get_request_parameter('id', converter=int, default=None)
		
		# Datastore Values
		target_ride = RideOffer.get_by_id(target_ride_id)
		
		# --------------------------------------------------------------------
		# Validate Request
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to the home page.
		if target_ride is None:
			self.error(404)
			return
		
		# --------------------------------------------------------------------
		# Generate and Store Template Values
		# --------------------------------------------------------------------
		template_values = super(ViewRideOfferPageHandler, self
			).generate_template_values(self.request.url)
		
		template_values['target_ride'] = target_ride

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "rideoffer_view.html")
		self.response.out.write(template.render(page_path, template_values))


# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Instalise web application
	application = webapp.WSGIApplication(
		[
		 ("/rideoffer_create", CreateRideOfferPageHandler),
		 ("/rideoffer_edit", EditRideOfferPageHandler),
		 ('/rideoffer', ViewRideOfferPageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
