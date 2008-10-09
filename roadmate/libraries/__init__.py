

import os
import sys


DIR_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

EXTRA_PATHS = [
	DIR_PATH
]

sys.path = EXTRA_PATHS + sys.path

import openid
import simplejson