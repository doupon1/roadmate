#!/usr/bin/env python

import os
import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.converters import is_true
from roadmate.google.googlemaps import GoogleMaps
from roadmate.handlers.baserequesthandler import BaseRequestHandler

from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.riderequest import RideRequest
from roadmate.models.riderequest import RideRequestForm
from roadmate.models.location import Location
from roadmate.models.message import RideRequestMessage

# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class ViewRideRequestPageHandler(BaseRequestHandler):
	"""
		RoadMate RequestHandler

		Page:
			/riderequest ( = riderequest_view.html)

		Get Arguments:
			id - Integer (Riderequest.key.id) [Required]
	"""
	def get(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and GET Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		# Request Values
		riderequest_id = self.get_request_parameter('id', converter=int, default=None)

		# Datastore Values
		riderequest = RideRequest.get_by_id(riderequest_id)

		# --------------------------------------------------------------------
		# Validate Request
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to the home page.
		if riderequest is None:
			self.error(404)
			return

		# --------------------------------------------------------------------
		# Generate and Store Template Values
		# --------------------------------------------------------------------
		template_values = super(ViewRideRequestPageHandler, self
			).generate_template_values(self.request.url)

		template_values['riderequest'] = riderequest
		template_values['googlemaps_key'] = GoogleMaps.get_key()
		template_values['message_list'] = list(riderequest.riderequestmessages.order('created'))


		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "riderequest_view.html")
		self.response.out.write(template.render(page_path, template_values))


	def post(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and GET Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		if current_user is None:
			self.redirect(users.create_login_url(self.request.url))
			return


		# Request Values
		riderequest_id = self.get_request_parameter('id', converter=int, default=None)

		# Datastore Values
		riderequest = RideRequest.get_by_id(riderequest_id)



		# --------------------------------------------------------------------
		# Validate Request
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to the home page.
		if riderequest is None:
			self.error(404)
			return

		# --------------------------------------------------------------------
		# Generate and Store Template Values
		# --------------------------------------------------------------------
		template_values = super(ViewRideRequestPageHandler, self
			).generate_template_values(self.request.url)

		template_values['riderequest'] = riderequest
		template_values['googlemaps_key'] = GoogleMaps.get_key()
		template_values['message_list'] = list(riderequest.riderequestmessages.order('created'))

		#if user is cancelling the riderequest
		if self.request.POST.has_key('do_cancel_request') and (current_user == riderequest.owner):
			riderequest.delete() #delete the riderequest
			self.redirect("/browse_riderequests") # redirect to the browse riderequest page
			return

		#if user is posting a message
		if self.request.POST.has_key('do_post_message') and self.request.POST['do_post_message']:
			message = RideRequestMessage(author=current_user, riderequest=riderequest, title=escape(self.request.POST['message_title']), text=escape(self.request.POST['message_body']))
			message.put()

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "riderequest_view.html")
		self.response.out.write(template.render(page_path, template_values))



class CreateRideRequestPageHandler(BaseRequestHandler):
	"""
		Create RideRequest

		Page:
			/riderequest_create (riderequest_create.html)

		Get Arguments:
			showSourceFavorites - Boolean [Default=False]
			showDestinationFavorites - Boolean [Default=False]
	"""

#GET REQUEST HANDLER
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
		template_values = super(CreateRideRequestPageHandler, self
			).generate_template_values(self.request.url)

		# because this page requires the user to be logged in, if they logout
		# we redirect them back to the home page.
		template_values['logout_url'] = users.create_logout_url("/")
		template_values['owner'] = current_user

		template_values['riderequest_form'] = RideRequestForm()

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "riderequest_create.html")
		self.response.out.write(template.render(page_path, template_values))

#POST REQUEST HANDLER
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
		# i.e. form has been submitted, do sth with the values
		# --------------------------------------------------------------------

		riderequest_data = { 'owner':current_user }

		riderequest_form = RideRequestForm(
			data=self.request.POST,
			initial=riderequest_data
		) #set a form for that instance

		# --------------------------------------------------------------------
		# Validate POST Data
		# --------------------------------------------------------------------
		# if there are errors in the form, then re-serve the page with the
		# error values highlighted.
		if not riderequest_form.is_valid():
			# ----------------------------------------------------------------
			# Generate Template Values
			# ----------------------------------------------------------------
			template_values = BaseRequestHandler.generate_template_values(self,
				self.request.url)


			# because this page requires the user to be logged in, if they
			# logout we redirect them back to the home page.
			template_values['logout_url'] = users.create_logout_url("/")
			template_values['owner'] = current_user

			template_values['riderequest_form'] = riderequest_form

			# ----------------------------------------------------------------
			# Render and Serve Template
			# ----------------------------------------------------------------
			page_path = os.path.join(os.path.dirname(__file__), "riderequest_create.html")
			self.response.out.write(template.render(page_path, template_values))
			return

		riderequest = riderequest_form.save() #else, the form is valid, so save it
		self.redirect("/riderequest?id=%s" % riderequest.key().id()) # redirect to the view page


# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/riderequest', ViewRideRequestPageHandler),
		 ('/riderequest_create', CreateRideRequestPageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
