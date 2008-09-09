

from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api.users import User

from google.appengine.ext.db import djangoforms

from roadmate.models.town import Town

class RoadMateUser(db.Model):
	"""
		RoadMate Data Model
		
		RoadUser
			Stores data about a site user.
	"""
	user = db.UserProperty(required=True)
	first_name = db.StringProperty()
	last_name = db.StringProperty()
	town = db.ReferenceProperty(Town)
	phone = db.PhoneNumberProperty()
	registration_date = db.DateTimeProperty(required=True, auto_now_add=True)
	
	def __eq__(self, other):
		"""Overloaded equality operator."""
		try:
			return self.key().id() == other.key().id()
		except:
			return NotImplemented
			
	def __ne__(self, other):
		"""Overloaded inequality opertator."""
		equality_result = (self == other)
		if equality_result is NotImplemented:
			return NotImplemented
		else:
			return not equality_result
	
	@classmethod
	def get_current_user(cls):
		"""Fetch an instance of RoadMateUser corrosponding to the current
		user.
		
		Returns:
			An instance of RoadMateUser which is in the datastore.
		"""
		current_user = users.get_current_user()
		
		if current_user is None:
			return None
		else:
			return cls.get_by_user(current_user, create=True)
	
	@classmethod
	def get_by_user(cls, user, create=False):
		"""Fetch or if necessary create an instance of RoadMateUser with the
		corrosponding user propertery.
		
		Args:
			user: An instance of google.appengine.api.users.User.
			create: Whether an instance of RoadMateUser should be created
				in the datastore if it does not exist.
			
		Returns:
			An instance of RoadMateUser which is in the datastore.
			
		Raises:
			KindError if user is not of kind google.appengine.api.users.User.
		"""
		# sanity checks
		if user is None:
			raise ValueError('user value must not be None')
		if not isinstance(user, User):
			raise KindError('Expected kind: %r, got kind: %r' %
				(User.kind(), user.kind()))
		
		# try to get the a RoadMateUser with a corrosponding user property
		roadmate_user = RoadMateUser.all().filter('user =', user).get()
		
		# if a corrosponding entity was not found in the datastore then create
		# one, if permitted.
		if not roadmate_user and create:
			roadmate_user = RoadMateUser(user=user)
			roadmate_user.put()
		
		return roadmate_user
		
	
class RoadMateUserForm(djangoforms.ModelForm):
	"""
		RoadMate Django ModelForm
		
		RoadUserForm
			Form for RoadMateUser.
	"""
	class Meta:
		model = RoadMateUser
		exclude = ['user', 'registration_date']
		
	