"""
	Collection of custom filters for the Django template framework.
"""


import re

from google.appengine.ext import webapp

from django.template.defaultfilters import date

from django.template.defaultfilters import time

register = webapp.template.create_template_register()

def local_part_from_email(value):
	return re.sub(r"(.*?)@(.*)", r"\1", value)

register.filter(local_part_from_email)

def date_for_table(value):
	return date(value, "d M Y")

register.filter(date_for_table)

def time_for_table(value):
	return time(value, "g:ia")

register.filter(time_for_table)
