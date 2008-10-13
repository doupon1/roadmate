#!/usr/bin/env python
# encoding: utf-8
"""Support for Google Calendar API."""

import os

class GoogleCalendar:
	"""A class providing Google Calendar functionality."""
	
	#: Google Calendar Keys
	_keys = {
		'localhost:8080':"ABQIAAAAh9vEamNAbo2MjViKEXyTSBQtrj2yXU7uUDf9MLK2OBnE3PD31hQrtHqCrQiA2FONyyl-gzfE04lUdA",
		'seat-web3.massey.ac.nz:8080':"ABQIAAAAh9vEamNAbo2MjViKEXyTSBQtrj2yXU7uUDf9MLK2OBnE3PD31hQrtHqCrQiA2FONyyl-gzfE04lUdA",
                'road-mate.appspot.com':"ABQIAAAAh9vEamNAbo2MjViKEXyTSBRhbta4VHtNWG2yNZ6nOJy0sL8GLhT3VwdjoVekwOUnlRQ9HE8X2T4JbQ"
	}
	
	@classmethod
	def get_key(cls):
		"""Returns the Google Calendar key assigned to the current host.
		
		@rtype:   unicode
		@returns: The Google Calendar key assigned to the current host.
		"""
		realm = os.environ.get('HTTP_HOST')
		
		if realm in cls._keys:
			return cls._keys[realm]
		else:
			raise ValueError(
				"The current host '%s' does not have a Google Calendar key." %
				(realm)
			)
