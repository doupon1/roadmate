#!/usr/bin/env python

import os
import re

from town import Town

# -----------------------------------------------------------------------------
#  Package Installisation
# -----------------------------------------------------------------------------
# Instalise static datastores
data_path = os.path.join(os.path.dirname(__file__), 'data')

# [Towns]
# import list of New Zealand towns from 'newzealand_towns.txt'
if Town.all().count() == 0:
	towns_path = os.path.join(data_path, 'newzealand_towns.txt')

	f_towns = open(towns_path)
	towns = f_towns.readlines()
	f_towns.close()

	for town in towns:
		d_town = Town(name=re.match('[\w ]+', town).group())
		d_town.put()