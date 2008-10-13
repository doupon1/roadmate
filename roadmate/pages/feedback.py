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
from django.template.defaultfilters import escape

from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.ride import Ride
from roadmate.models.seat import Seat
from roadmate.models.message import FeedbackMessage
from roadmate.models.message import FeedbackForm



# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class ViewFeedbackPageHandler(BaseRequestHandler):
	"""
		View the list of received feedback for a given user

		Page:
			/feedback ( = feedback.html)

		Get Arguments:
			id - Integer (RoadMateUser.key.id) [Required]
	"""
	def get(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and GET Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		# Request Values
		target_user_id = self.get_request_parameter('id', converter=int, default=None)

		# Datastore Values
		target_user = RoadMateUser.get_by_id(target_user_id)

		# --------------------------------------------------------------------
		# Validate Request
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to the home page.
		if target_user is None:
			self.error(404)
			return
		# --------------------------------------------------------------------
		# Generate and Store Template Values
		# --------------------------------------------------------------------
		template_values = super(ViewFeedbackPageHandler, self
			).generate_template_values(self.request.url)

		template_values['target_user'] = target_user
		template_values['feedback_list'] = list(target_user.feedback_received)
		template_values['count_positive'] = target_user.feedback_received.filter('value=', 1).count()
		template_values['count_neutral'] = target_user.feedback_received.filter('value=', 0).count()
		template_values['count_negative'] = target_user.feedback_received.filter('value=', -1).count()

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "feedback.html")
		self.response.out.write(template.render(page_path, template_values))






class CreateFeedbackPageHandler(BaseRequestHandler):
	"""
		Place feedback on a RoadMateUser concerning a ride

		The handler infers the relationship (passenger on driver, or driver on passenger)
		between the current_user and the RoadMateUser specified in the "on" get param.

		If it is invalid (one or both actors not belonging to the ride specified in the "ride" param,
		then it errors out. It also errors if feedback has been placed before. Actors only get one
		chance to place feedback.

		Page:
			/feedback_create (feedback_create.html)

		GET params:
		    ride   (int) ID of the Ride that the feedback to create relates to
		    on     (int) ID of the RoadMateUser who is receiving the feedback
	"""

#GET REQUEST HANDLER
	def get(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and Request Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		# Request Values
  		ride_id = self.get_request_parameter('ride', converter=int, default=None)
  		target_user_id = self.get_request_parameter('on', converter=int, default=None)

  		# Retrieve the instances
  		ride = Ride.get_by_id(ride_id)
   		target_user = RoadMateUser.get_by_id(target_user_id)
	  	feedback_form = FeedbackForm()
		target_user_role = '' # empty by default


		# --------------------------------------------------------------------
		# Validate Session and Request
		# --------------------------------------------------------------------
		# if the current users in not logged in, then we redirect them through
		# a login page.
  		if current_user is None:
			self.redirect(users.create_login_url(self.request.url))
			return
		# if the target user is not valid then error
		if target_user is None or ride is None:
			self.error(403) # forbidden
			return

		# if the target user is not the driver, and the current user is not a passenger
		# or vice versa, then error
		if ride.is_passenger(current_user) and (target_user == ride.owner):
			target_user_role = 'driver'
		elif ride.is_passenger(target_user) and (current_user == ride.owner):
			target_user_role = 'passenger'
		else: # then the relationship is not valid
			self.error(403) # forbidden
			return

		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = super(CreateFeedbackPageHandler, self
			).generate_template_values(self.request.url)

		# because this page requires the user to be logged in, if they logout
		# we redirect them back to the home page.
		template_values['logout_url'] = users.create_logout_url("/")
		template_values['owner'] = current_user
		template_values['target_user'] = target_user
		template_values['ride'] = ride
		template_values['feedback_form'] = feedback_form
		template_values['target_user_role'] = target_user_role

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "feedback_create.html")
		self.response.out.write(template.render(page_path, template_values))

#POST REQUEST HANDLER
	def post(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and Request Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		# Request Values
  		ride_id = self.get_request_parameter('ride', converter=int, default=None)
  		target_user_id = self.get_request_parameter('on', converter=int, default=None)

  		# Retrieve the instances
  		ride = Ride.get_by_id(ride_id)
   		target_user = RoadMateUser.get_by_id(target_user_id)
   		feedback_form = FeedbackForm()
		target_user_role = '' # empty by default


		# --------------------------------------------------------------------
		# Validate Session and Request
		# --------------------------------------------------------------------
		# if the current users in not logged in, then we redirect them through
		# a login page.
  		if current_user is None:
			self.redirect(users.create_login_url(self.request.url))
			return
		# if the target user is not valid then error
		if target_user is None or ride is None:
			self.error(403) # forbidden
			return
		#if the current user has already placed feedback on the author for this ride
		if ride.feedbackmessages.filter('author =', current_user).filter('recipient =', target_user):
			self.redirect("/feedback?id=%s" % target_user.key().id()) # redirect to the recipient's feedback page
			return


		# if the target user is not the driver, and the current user is not a passenger
		# or vice versa, then error
		if ride.is_passenger(current_user) and (target_user == ride.owner):
			target_user_role = 'passenger'
		elif ride.is_passenger(target_user) and (current_user == ride.owner):
			target_user_role = 'driver'
		else: # then the relationship is not valid
			self.error(403) # forbidden
			return


## not working
##		# --------------------------------------------------------------------
##		# Retrive POST Data
##		# and create a new instance of the form to validate the data
##		# --------------------------------------------------------------------
##		feedback_data = { 'author': current_user, 'ride':ride, 'recipient':target_user, 'role': target_user_role}
##
##		feedback_form = FeedbackForm(
##			data=self.request.POST,
##			initial=feedback_data
##		) # create the form to validate
##		print(feedback_form['ride'].data)
##
##		# --------------------------------------------------------------------
##		# Validate POST Data
##		# --------------------------------------------------------------------
##		# if there are errors in the form, then re-serve the page with the
##		# error values highlighted.
##		if not feedback_form.is_valid():
##			# ----------------------------------------------------------------
##			# Generate Template Values
##			# ----------------------------------------------------------------
##			template_values = BaseRequestHandler.generate_template_values(self,
##				self.request.url)
##
##			# because this page requires the user to be logged in, if they
##			# logout we redirect them back to the home page.
##			template_values['logout_url'] = users.create_logout_url("/")
##
##			# --------------------------------------------------------------------
##			# Set up the page 'passenger' or 'driver' display
##			# --------------------------------------------------------------------
##			target_user_role = 'driver' # by default
##			if ride.is_passenger(target_user):
##				target_user_role = 'passenger'
##
##			# --------------------------------------------------------------------
##			# Generate Template Values
##			# --------------------------------------------------------------------
##			template_values = super(CreateFeedbackPageHandler, self
##				).generate_template_values(self.request.url)
##
##			# because this page requires the user to be logged in, if they logout
##			# we redirect them back to the home page.
##			template_values['logout_url'] = users.create_logout_url("/")
##			template_values['owner'] = current_user
##			template_values['target_user'] = target_user
##			template_values['ride'] = ride
##			template_values['feedback_form'] = feedback_form
##			template_values['target_user_role'] = target_user_role
##
##			# ----------------------------------------------------------------
##			# Render and Serve Template
##			# ----------------------------------------------------------------
##			print(feedback_form.errors)
##			page_path = os.path.join(os.path.dirname(__file__), "feedback_create.html")
##			self.response.out.write(template.render(page_path, template_values))
##			return

		feedback_message = FeedbackMessage(
						 ride=ride,
						 author=current_user,
						 recipient=target_user,
						 role=target_user_role,
				   		 value=int(self.request.POST['value']),
				   		 text=escape(self.request.POST['text'])
						 ) # not validated

		feedback_message.put() # save the new Message
		self.redirect("/feedback?id=%s" % target_user.key().id()) # redirect to the recipient's profile page or feedback page



# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/feedback_create', CreateFeedbackPageHandler),
		 ('/feedback', ViewFeedbackPageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()

