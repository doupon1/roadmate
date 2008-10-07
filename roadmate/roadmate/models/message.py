from google.appengine.ext import db

from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.ride import Ride

class Message(db.Model):
	"""
		Message
			   A message posted on a Ride by a RoadMateUser to facilitate discussion
			   about the Ride so the owner, passengers, and potential passengers can ask questions
			   and clarify the circumstances of the ride.

		Usage:
			  Use the 'created' attribute to display the messages in chronological order
			  The 'title' and 'text' attributes should be plain text, validated for tags and malicious code
	"""

	author = db.ReferenceProperty(RoadMateUser, collection_name="messages", required=True) #the user who has written the message
	created = db.DateTimeProperty(required=True, auto_now_add=True) #date the message was created - this is how the messages should be ordered
	ride = db.ReferenceProperty(Ride, collection_name="messages", required=True) #the ride which the message relates to
	title = db.TextProperty() #the title text of the message
	text = db.TextProperty() #the body text of the message

	# for changing the display style of a message based on its author
	# return "user", "passenger", or "driver"
	# matching css tags in table. and td. on higher_ground.css
	def style(self):
		if self.author == self.ride.owner:
			return "driver"
		elif self.ride.is_passenger(self.author):
			return "passenger"
		else:
			return "user"

	def __unicode__(self):
		"""Returns a string representation of the object."""
		return self.title()

