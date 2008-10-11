from google.appengine.ext import db

from google.appengine.ext.db import djangoforms
from django import newforms as forms

from roadmate.models.roadmateuser import RoadMateUser
from roadmate.models.ride import Ride
from roadmate.models.riderequest import RideRequest


class Message(db.Model):
	"""
		Message (abstract)

				Do not instantiate directly, use the derived classes

		Usage:
			  Use the 'created' attribute to display the messages in chronological order
			  The 'title' and 'text' attributes should be plain text, validated for tags and malicious code
	"""
	created = db.DateTimeProperty(required=True, auto_now_add=True) #date the message was created - this is how the messages should be ordered
	title = db.TextProperty() #the title text of the message
	text = db.TextProperty() #the body text of the message

	def __unicode__(self):
		"""Returns a string representation of the object."""
		return self.title()

class RideMessage(Message):
	"""
	   RideMessage
			   A message posted by a RoadMateUser on a ride to facilitate discussion
			   about the Ride so the owner, passengers, and potential passengers can ask questions
			   and clarify the circumstances of the ride.

	"""
	ride = db.ReferenceProperty(Ride, collection_name="ridemessages", required=True) #the ride which the message relates to
	author = db.ReferenceProperty(RoadMateUser, collection_name="ridemessages", required=True) #the user who has written the message

	# for changing the display style of a RideMessage based on its author
	# return "user", "passenger", or "owner"
	# matching css tags in table. and td. on higher_ground.css
	def style(self):
		if self.author == self.ride.owner:
			return "owner"
		elif self.ride.is_passenger(self.author):
			return "passenger"
		else:
			return "user"

class RideRequestMessage(Message):
	"""
	   RideRequestMessage
		   A message posted by a RoadMateUser on a RideRequest to facilitate discussion
		   about the RideRequest so the owner, passengers, and potential passengers can ask questions
		   and clarify the circumstances of the ride.
	"""
	riderequest = db.ReferenceProperty(RideRequest, collection_name="riderequestmessages", required=True) #the ride which the message relates to
	author = db.ReferenceProperty(RoadMateUser, collection_name="riderequestmessages", required=True) #the user who has written the message

	# for changing the display style of a RideRequestMessage based on its author
	# return "user" or "owner"
	# matching css tags in table. and td. on higher_ground.css
	def style(self):
		if self.author == self.riderequest.owner:
			return "owner"
		else:
			return "user"

class FeedbackMessage(Message):
	"""
	   FeedbackMessage
		   A message and social score placed against another user, either by a passenger on a driver, or vice versa
		   Other users can view these and make a personal judgment about whether the person
		   is acceptable to travel with

	"""
	ride = db.ReferenceProperty(Ride, collection_name="feedbackmessages", required=True) #the ride which the feedback relates to
	author = db.ReferenceProperty(RoadMateUser, collection_name="feedback_placed", required=True) #the user who has written the message
	recipient = db.ReferenceProperty(RoadMateUser, collection_name="feedback_received", required=True) #the user that the message is about
	value = db.IntegerProperty(default=0) # these can be summed to give the 'social score' of the recipient
	role = db.TextProperty() # the role (passenger or driver) that the feedback relates to

	#returns the correct 'face' image filename according to the value attribute
	def icon(self):
		if self.value == 1:
			return '<img src="/images/positive_fb.gif"/ >'
		elif self.value == 0:
			return '<img src="/images/neutral_fb.gif"/ >'
		elif self.value == -1:
			return '<img src="/images/negative_fb.gif"/ >'
		else:
			return 'Error: invalid value' #debug


class FeedbackForm(djangoforms.ModelForm):
	"""
	   Form to create Feedback

			The feedback image TAGS are the 'key' parameter in the choices (list of 2-tuples)
	"""
	value = forms.ChoiceField(
		widget=forms.RadioSelect,
		choices=[(1,'<img src="/images/positive_fb.gif"/ >'),(0,'<img src="/images/neutral_fb.gif"/ >'),(-1,'<img src="/images/negative_fb.gif"/ >')]
		)

	class Meta:
		  model = FeedbackMessage
		  exclude = ['author', 'created', 'title']
