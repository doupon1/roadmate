

from google.appengine.api import users
from google.appengine.ext import webapp

class BaseRequestHandler(webapp.RequestHandler):
	"""
		RoadMate RequestHandler
		
		Pages:
			/templates/base.html
	"""
	
	def generate_template_values(self, page_url):
		"""
			generate_template_values
			
			Generates a dictionary of template values required by the pages
			served from this request handler.
			
			Parameters:
				page_url - The URL of the page requesting the template values.
			
		"""
		
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		current_user = users.get_current_user()

		isLoggedIn = False
		if current_user:
			isLoggedIn = True

		login_url = users.create_login_url(page_url)
		logout_url = users.create_logout_url(page_url)

		# --------------------------------------------------------------------
		# Store Template Values
		# --------------------------------------------------------------------
		template_values = {}
		
		template_values['current_user'] = current_user
		template_values['isLoggedIn'] = isLoggedIn
		template_values['login_url'] = login_url
		template_values['logout_url'] = logout_url
		
		return template_values
		
		