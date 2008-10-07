#!/usr/bin/env python
# encoding: utf-8
"""Support for Google Maps API."""

import os
import logging
import urllib

from google.appengine.api import urlfetch

class GoogleMaps:
	"""A class providing Google Maps functionality."""
	
	#: Google Maps Keys
	_keys = {
		'localhost:8080':"ABQIAAAALrh5mwxiKkNrHuqNwGGHJRTwM0brOpm-All5BF6PoaKBxRWWERQ6Ykd3tAT6M4xWsQW4l2QU6snihg",
		'seat-web3.massey.ac.nz:8080':"ABQIAAAALCi9t1naIjEhwoF3_R48QxQtrj2yXU7uUDf9MLK2OBnE3PD31hRS8GRlNBL8LAzbUwLiBPN_wWqmoQ"
	}
	
	@classmethod
	def get_key(cls):
		"""Returns the Google Maps key assigned to the current host.
		
		@rtype:	  unicode
		@returns: The Google Maps key assigned to the current host.
		
		@raises ValueError: When the current host does not have a google maps
			key assigned to it.
		"""
		realm = os.environ.get('HTTP_HOST')
		
		if realm in cls._keys:
			return cls._keys[realm]
		else:
			raise ValueError(
				"The current host '%s' does not have a Google Maps key" %
				(realm)
			)
		
	@classmethod
	def get_lat_loc(cls, address):
		"""Returns a string that contains the latitude and longitude of the
		location.
		
		@type  address: unicode
		@param address: A string containing the address to look up.
		
		@rtype:	  unicode
		@returns: A string containing the latitude and longitude of the
			location, if the lookup was successful. Else an empty string
			is returned.
		"""
		output = "csv"
		location = urllib.quote_plus(address)
		url = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % \
			(location, output, GoogleMaps.get_key())
		
		try:
			content = urlfetch.fetch(url).content
			dlist = content.split(',')
			
			status_code = dlist[0]
			latitude = dlist[2]
			longitude = dlist[3]
			
			if status_code == '200':
				return "%s, %s" % (latitude, longitude)
			else:
				return ''
		except Exception:
			logging.error(
				"GoogleMaps.get_lat_loc failed for address '%s'" %
				(address)
			)
			return ''