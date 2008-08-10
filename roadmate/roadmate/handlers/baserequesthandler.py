
from google.appengine.api import users
from google.appengine.ext import webapp

class BaseRequestHandler(webapp.RequestHandler):
	"""
		RoadMate RequestHandler
		
		Pages:
			/templates/base.html
	"""
	
	def get_request_parameter(self, name, converter=None, default=None):
		"""docstring for get_request_parameter"""
		request_value = self.request.get(name)
		
		if request_value == "":
			return default
		
		if converter is not None:
			try:
				return converter(request_value)
				
			except (TypeError, ValueError):
				return default
		
		return request_value
	
	def generate_template_values(self, page_url):
		"""	Generates a dictionary of template values required by the pages
			served from this request handler.
			
			Parameters:
				page_url - The URL of the page requesting the template values.
			
		"""
		
		# --------------------------------------------------------------------
		# Generate Template Values
		# --------------------------------------------------------------------
		current_user = users.get_current_user()
		current_version = "0.1" ## update me

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
		template_values['current_version'] = current_version
		template_values['isLoggedIn'] = isLoggedIn
		template_values['login_url'] = login_url
		template_values['logout_url'] = logout_url
		
		return template_values
		
		