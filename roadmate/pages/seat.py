#!/usr/bin/env python
#TODO tidy up references in these handler pages,
import os
import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.handlers.baserequesthandler import BaseRequestHandler
from roadmate.models.roadmateuser import RoadMateUser

from roadmate.models.seat import Seat
from roadmate.models.seat import SeatForm

# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class ViewSeatPageHandler(BaseRequestHandler):
	"""
		RoadMate RequestHandler

		Pages:
			/seat ( = seat_view.html)

			TODO Eventually want to merge view and assign seat pages
			so that owners can assign/edit from the view page if they are logged in

		Get Arguments:
			id - Integer (Seat.key.id) [Required]
	"""

	def get(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and GET Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()


		# Request Values
		seat_id = self.get_request_parameter('id', converter=int, default=None)

		# Datastore Values
		seat = Seat.get_by_id(seat_id)
		# --------------------------------------------------------------------
		# Validate Request
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to the home page.
		if seat is None:
			self.error(404)
			return

		# --------------------------------------------------------------------
		# Generate and Store Template Values
		# --------------------------------------------------------------------
		template_values = super(ViewSeatPageHandler, self
			).generate_template_values(self.request.url)

		template_values['seat'] = seat


		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "seat_view.html")
		self.response.out.write(template.render(page_path, template_values))




class AssignSeatPageHandler(BaseRequestHandler):
	"""
		GET a Seat by its ID and show its details

		Page:
			/seat_assign (seat_assign.html)

		GET Arguments:
			id - Integer (Seat.key.id) [Required]

		POST Parameters:
			_id - Integer (Seat.key.id) [Required]
	"""
	def get(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and Request Data
		# --------------------------------------------------------------------
		# Session Values
		current_user = RoadMateUser.get_current_user()

		# Request Values
		seat_id = self.get_request_parameter('id', converter=int, default=None)

		# Datastore Values
		seat = Seat.get_by_id(seat_id)

		# --------------------------------------------------------------------
		# Validate Session and Request
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to the home page.
		if seat is None:
			self.error(404)
			return


		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		template_values = super(AssignSeatPageHandler, self
			).generate_template_values(self.request.url)

		# because the user is viewing the page in edit mode, then logging out
		# should redirect to the read-only version.
		template_values['logout_url'] = users.create_logout_url(
			"/seat?id=%s" % seat.key().id())

		template_values['seat'] = seat


		# --------------------------------------------------------------------
		# Set up the selection values dynamically
		# --------------------------------------------------------------------
		seat_form = SeatForm(instance=seat)
		prq = seat.ride.passengerrequests
		selections = tuple()
		for request in prq:
				selections.__add__(request.owner.key,request.owner.key)
		seat_form.fields['selection'].choices = selections
		#print(dir(seat_form.fields['passenger'].choices))


  		# --------------------------------------------------------------------
		# Add the form to the template values
		# --------------------------------------------------------------------
		template_values['assign_seat_form'] = seat_form

		# --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		page_path = os.path.join(os.path.dirname(__file__), "seat_assign.html")

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
		seat_id = self.get_request_parameter('_id', converter=int, default=None)
		seat = Seat.get_by_id(seat_id)

		# --------------------------------------------------------------------
		# Validate POST Data
		# --------------------------------------------------------------------
		# if the target ride does not exist in the datastore, then redirect
		# the user back to an error page.
		if seat is None:
			self.error(404)
			return

		# if the user is trying to edit a ride they did not create,
		# redirect them to an error page (403: Forbidden).
		if seat.owner != current_user:
			logging.warning("User '%s' attempted to edit a ride offer"\
				" belonging to user '%s'. Redirecting to an error page."  %
				(current_user.user.email, rideoffer.owner.user.email))

			self.error(403)
			return

		assign_seat_form = SeatForm(
			data=self.request.POST,
			instance=seat
		)

		# if there are errors in the form, then re-serve the page with the
		# error values highlighted.
		if not assign_seat_form.is_valid():
			# ----------------------------------------------------------------
			# Generate Template Values
			# ----------------------------------------------------------------
			template_values = super(AssignSeatPageHandler, self
				).generate_template_values(self.request.url)

			# because this page requires the user to be logged in, if they
			# logout we redirect them back to the home page.
			template_values['logout_url'] = users.create_logout_url("/")

			template_values['assign_seat_form'] = assign_seat_form

			# ----------------------------------------------------------------
			# Render and Serve Template
			# ----------------------------------------------------------------
			page_path = os.path.join(os.path.dirname(__file__), "seat_assign.html")
			self.response.out.write(template.render(page_path, template_values))
			return

		# --------------------------------------------------------------------
		# Finalise POST Request
		# --------------------------------------------------------------------
		assign_seat_form.save()
		self.redirect("/seat?id=%s" % seat.key().id())


# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/seat', ViewSeatPageHandler),
		 ('/seat_assign', AssignSeatPageHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()


