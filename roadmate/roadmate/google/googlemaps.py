#!/usr/bin/env python
# encoding: utf-8
"""Support for Google Maps API."""

import os
import logging
import urllib

from google.appengine.api import urlfetch
from google.appengine.ext.db import GeoPt

class GoogleMaps:
	"""A class providing Google Maps functionality."""
	
	#: Google Maps Keys
	_keys = {
		'localhost:8080':"ABQIAAAALrh5mwxiKkNrHuqNwGGHJRTwM0brOpm-All5BF6PoaKBxRWWERQ6Ykd3tAT6M4xWsQW4l2QU6snihg",
		'seat-web3.massey.ac.nz:8080':"ABQIAAAALCi9t1naIjEhwoF3_R48QxQtrj2yXU7uUDf9MLK2OBnE3PD31hRS8GRlNBL8LAzbUwLiBPN_wWqmoQ",
		'road-mate.appspot.com':"ABQIAAAALCi9t1naIjEhwoF3_R48QxRhbta4VHtNWG2yNZ6nOJy0sL8GLhQmdrJBrmpLe3AZgiflnsysMODZWQ"
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
	def is_valid_address(cls, address):
		"""Returns True if the given address exists in the Google Maps 
		database.
		
		@type  address: unicode
		@param address: A string containing the address to validate.
		
		@rtype:   bool
		@returns: True if the address is valid.
		"""
		return GoogleMaps.get_lat_loc(address) != ''
		
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
			
	@classmethod
	def get_geo_point(cls, address):
		"""Returns a GeoPt for the given address. None if it does not exist.
		"""
		lat_long = GoogleMaps.get_lat_loc(address)
		
		if lat_long != '':
			address_lat, address_long = lat_long.split(', ')
			return GeoPt(float(address_lat), float(address_long))
		else:
			return None
		