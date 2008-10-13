#!/usr/bin/env python
# encoding: utf-8

import os
import urllib
import logging
import math

import simplejson

from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from roadmate.models.ride import Ride
from roadmate.handlers.baserequesthandler import BaseRequestHandler

from roadmate.models.location import Location

# ----------------------------------------------------------------------------
#  Constants
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
#  Request Handlers
# ----------------------------------------------------------------------------

class LocationFinderRequestHandler(BaseRequestHandler):
	"""Locates address lying within the bounds of the circle.

		Page:
			/

		Get Arguments:
                        srcCircleCenterLat - float[Required]
                        srcCircleCenterLng - float[Required]
                        desCircleCenterLat - float[Required]
                        desCircleCenterLng - float[Required]
                        srcRadius - float[Required]
                        desRadius - float[Required]
	"""
	def post(self):
		# --------------------------------------------------------------------
		# Retrive Session Info and GET Data
		# --------------------------------------------------------------------
		# Request Values
		srcCircleCenterLat = self.get_request_parameter('srcCircleCenterLat', converter=float, default=None)
		srcCircleCenterLng = self.get_request_parameter('srcCircleCenterLng', converter=float, default=None)
                desCircleCenterLat = self.get_request_parameter('desCircleCenterLat', converter=float, default=None)
		desCircleCenterLng = self.get_request_parameter('desCircleCenterLng', converter=float, default=None)
		srcRadius = self.get_request_parameter('srcRadius', converter=float, default=None)
		desRadius = self.get_request_parameter('desRadius', converter=float, default=None)
		
		logging.info("srcCircle center lat: %s,srcCircle center lng: %s, srcCircle Radius %d, desCircle center lat: %s,desCircle center lng: %s, desCircle Radius %d" %
                             (srcCircleCenterLat, srcCircleCenterLng, srcRadius, desCircleCenterLat, desCircleCenterLng, desRadius))

		# --------------------------------------------------------------------
		# Validate Request
		# --------------------------------------------------------------------
		if srcCircleCenterLat is None:
			self.error(400)
			return
		if srcCircleCenterLng is None:
			self.error(400)
			return
		if srcRadius is None:
			self.error(400)
			return
		if desCircleCenterLat is None:
			self.error(400)
			return
		if desCircleCenterLng is None:
			self.error(400)
			return
		if desRadius is None:
			self.error(400)
			return
		# --------------------------------------------------------------------
		# Generate and Store Template Values
		# --------------------------------------------------------------------
		#Convert srcRadius from meters to Kilometers
		srcR = srcRadius/1000
		desR = desRadius/1000
		validPoints = []

		rides = db.GqlQuery("SELECT * FROM Ride")
		
		for ride in rides:
			current_src = ride.source.get_lat_loc()
			current_des = ride.destination.get_lat_loc()
			srcLat, srcLon = current_src.split(", ")
			desLat, desLon = current_des.split(", ")
			
			srcLat = float(srcLat)
			srcLon = float(srcLon)
			desLat = float(desLat)
			desLon = float(desLon)
			
			state1 = checkpoint(srcR, srcCircleCenterLat, srcCircleCenterLng , srcLat, srcLon)
			state2 = checkpoint(desR, desCircleCenterLat, desCircleCenterLng , desLat, desLon)
			if(state1 == True & state2 == True):
				validPoints.append(ride)
		list_lats_lngs = str(validPoints)
                # --------------------------------------------------------------------
		# Render and Serve Template
		# --------------------------------------------------------------------
		self.response.out.write(simplejson.dumps(validPoints, default=encode_ride))

#Checks whether a point lies within the circle with center
def checkpoint (circleRad, centerLat, centerLng , pointLat, pointLng):
        logging.info("Radius: %f, CLat: %f, CLng: %f, PLat: %f, PLng: %f" % (circleRad, centerLat, centerLng , pointLat, pointLng))
        
	r = 6371.0
	lon1 = centerLng * math.pi / 180.0;
	lat1 = centerLat * math.pi / 180.0;
	lon2 = pointLng * math.pi / 180.0;
	lat2 = pointLat * math.pi / 180.0;

	deltaLat = lat1 - lat2
	deltaLon = lon1 - lon2

	step1 = math.pow(math.sin(deltaLat/2.0), 2) + math.cos(lat2) * math.cos(lat1) * math.pow(math.sin(deltaLon/2.0), 2)
	step2 = 2.0 * math.atan2(math.sqrt(step1), math.sqrt(1.0 - step1))

	distance = step2 * r

	logging.info("Dist: %f" % distance)

	if(distance < circleRad):
		return True
	else:
		return False

def encode_ride(ride):
	srcLatLng = ride.source.get_lat_loc()
	srcLat, srcLng = srcLatLng.split(", ")

 	desLatLng = ride.destination.get_lat_loc()
	desLat, desLng = desLatLng.split(", ")
	return {
		"id" : ride.key().id(),
		"source" :
			{
				"id" : ride.source.key().id(),
				"lat" : srcLat,
				"lng" : srcLng
			},
		"destination" :
			{
				"id" : ride.destination.key().id(),
				"lat" : desLat,
				"lng" : desLng
			}
		}

# ----------------------------------------------------------------------------
#  Program Entry Point
# ----------------------------------------------------------------------------

def main():
	# Initialize web application
	application = webapp.WSGIApplication(
		[
			('/ajax/location-finder', LocationFinderRequestHandler)
		], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
	main()
