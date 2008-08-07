"""
	Collection of custom conversion functions.
"""

def is_true(value):
	"""	Returns a boolean indicating whether the given value equals the
		string 'True' or some varient thereof.
	"""
	value = value.lower()
	
	return (
		(value == "true") |
		(value == "t") |
		(value == "yes") |
		(value == "y")
	)