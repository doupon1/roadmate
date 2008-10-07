#!/usr/bin/env python
# encoding: utf-8
"""Support for Google Calendar API."""

from os

class GoogleMaps:
	"""A class providing Google Calendar functionality."""
	
	#: Google Calendar Keys
	_keys = {
		'localhost:8080':"",
		'seat-web3.massey.ac.nz:8080':""
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