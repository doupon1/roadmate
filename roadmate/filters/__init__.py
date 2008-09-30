"""
	Collection of custom filters for the Django template framework.
"""

import re
from google.appengine.ext import webapp
 
register = webapp.template.create_template_register()
 
def local_part_from_email(email_address):
	return re.sub(r"(.*?)@(.*)", r"\1", email_address)
 
register.filter(local_part_from_email)