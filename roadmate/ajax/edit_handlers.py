import os
import logging


from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from roadmate.converters import is_true
from roadmate.handlers.baserequesthandler import BaseRequestHandler
from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.riderequest import RideRequest




class EditProfileHandler(BaseRequestHandler):
	"""
		Handles AJAX requests to change attribute values of a RoadMateUser without reloading the page

		Produces a text 'page' which is just the new text value for the requesting control

		GET Arguments:
			user - Integer (RoadMateUser.key.id) [Required]
		POST Arguments:
			 editorId - String - The attribute to change
			 value - String - The new value of the attribute
	"""
	def post(self):
		# --------------------------------------------------------------------
		# Retrive and Validate Request
		# --------------------------------------------------------------------
		# Default Values
		current_user = RoadMateUser.get_current_user()

		# --------------------------------------------------------------------
		# Validate Sesson
		# --------------------------------------------------------------------
		# if the current users in not logged in, then we redirect them through
		# a login page.
		if current_user is None:
			self.redirect(users.create_login_url(self.request.url))
			return
		target_user = None

		# --------------------------------------------------------------------
		# Retrieve user from GET Data, return the user
		# --------------------------------------------------------------------
		target_user_id = self.get_request_parameter('user', converter=int, default=None)
		target_user = RoadMateUser.get_by_id(target_user_id)

		# --------------------------------------------------------------------
		# Validate the user and POST Data
		# --------------------------------------------------------------------
		# if the target user does not exist in the datastore, then redirect
		# the user back to an error page.
		if target_user is None:
			self.error(404)
			return

		# if the user is trying to edit someone elses profile page,
		# then present them with an error page (403: Forbidden).
		if target_user != current_user:
			logging.error("User '%s' attempted to modify the profile of"\
				" user '%s'. Redirecting to error page." %
				(current_user.user.email, target_user.user.email))
			self.error(403)
			return

		# --------------------------------------------------------------------
		# Set the changed attribute and save the entity
		# --------------------------------------------------------------------

		if self.request.POST.has_key('editorId') and self.request.POST.has_key('value'):
			 # input text must not be "None" (the default NULL representation)
			 # and must not try to set a private attribute (which all start with '_')
			if not self.request.POST['value'] == "None" and not self.request.POST['editorId'].startswith('_'):
				setattr(target_user, self.request.POST['editorId'], self.request.POST['value'])# update that attribute
				target_user.save() # save the record
				self.response.out.write(getattr(target_user, self.request.POST['editorId'])) # print that value to the page
			else: # input text is "None", return the same
				self.response.out.write("None")
		else: # values are missing
			self.error(403)





class EditRideRequestHandler(BaseRequestHandler):
	"""
		Handles AJAX requests to change attributes values of a RideRequest without reloading the page

		Produces a text 'page' which is just the new text value for the requesting control

		GET Arguments:
			id - Integer (RideRequest.key.id) [Required]
		POST Arguments:
			 editorId - String - The attribute to change
			 value - String - The new value of the attribute
	"""
	def post(self):
		# --------------------------------------------------------------------
		# Retrive and Validate Request
		# --------------------------------------------------------------------
		# Default Values
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
		# Retrieve user from GET Data, return the user
		# --------------------------------------------------------------------
		# Request Values
		riderequest_id = self.get_request_parameter('id', converter=int, default=None)

		# Datastore Values
		riderequest = RideRequest.get_by_id(riderequest_id)

		# --------------------------------------------------------------------
		# Validate the user and POST Data
		# --------------------------------------------------------------------
		# if the entity does not exist in the datastore, then redirect
		# the user back to an error page.
		if riderequest is None:
			self.error(404)
			return

		# if the user is trying to edit an entity not belonging to them
		# then present them with an error page (403: Forbidden).
		if riderequest.owner != current_user:
			logging.error("User '%s' attempted to edit a riderequest '%s' which does not belong to them"\
				"Redirecting to error page." %
				(current_user.user.email, riderequest.key.id))
			self.error(403)
			return

		# --------------------------------------------------------------------
		# Set the changed attribute and save the entity
		# --------------------------------------------------------------------

		if self.request.POST.has_key('editorId') and self.request.POST.has_key('value'):
			 # input text must not be "None" (the default NULL representation)
			 # and must not try to set a private attribute (which all start with '_')
			if not self.request.POST['value'] == "None" and not self.request.POST['editorId'].startswith('_'):
				setattr(riderequest, self.request.POST['editorId'], self.request.POST['value'])# update that attribute
				riderequest.save() # save the record
				self.response.out.write(getattr(riderequest, self.request.POST['editorId'])) # print that value to the page
			else: # input text is "None", return the same
				self.response.out.write("None")
		else: # values are missing
			self.error(403)









# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web  application
	application = webapp.WSGIApplication(
		[
		 ('/edit_profile', EditProfileHandler),
		 ('/edit_riderequest', EditRideRequestHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
