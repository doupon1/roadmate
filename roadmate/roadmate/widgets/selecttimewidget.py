import re

from django.newforms.widgets import Widget, Select
from django.utils.dates import MONTHS


class SelectTimeWidget(Widget):
	"""
	A Widget that displays time input as a <select> box in 30 min increments.
	"""
	time_field = '%s_time'

	def render(self, name, value, attrs=None):
		output = []

		time_choices = []
		time_choices.append(("00:00", "12:00am"))
		time_choices.append(("00:00", "12:30am"))
		
		for hour in range (1, 12):
			hour = str(hour)
			time_choices.append((hour + ":00", hour + ":00am"))
			time_choices.append((hour + ":30", hour + ":30am"))
			
		time_choices.append(("12:00", "12:00pm"))
		time_choices.append(("12:30", "12:30pm"))
			
		for hour in range (1, 12):
			hour_12 = str(hour)
			hour_24 = str(hour + 12)
			time_choices.append((hour_24 + ":00", hour_12 + ":00pm"))
			time_choices.append((hour_24 + ":30", hour_12 + ":30pm"))

		select_html = Select(choices=time_choices).render(self.time_field % name, value)
		output.append(select_html)

		return u'\n'.join(output)

	def value_from_datadict(self, data, name):
		return data.get(self.time_field % name)

