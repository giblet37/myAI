"""
Global settings are stored here
"""

import logging
import sys

from os import mkdir, path
from os.path import join
from sys import platform as _platform

import api_library
import modules as active_mods



# OpenWeatherMap API info
OWM_API_KEY = 'KEY'
OWM_STATE = 'QNS'
OWM_LOCATION = 'Brisbane'
OWM_UNITS = 'metric'
OWM_TEMPUNIT = 'celsius'
OWM_HOT_TEMP = 32 #anything over 32 degrees celsius is concidered hot
OWM_COLD_TEMP = 20 #anything over 20 degrees celsius is cold

#####################
#    DIRECTORIES    #
#####################
CLIENT_DIR =    path.dirname(path.abspath(__file__))
BASE_DIR =      path.dirname(CLIENT_DIR)
DATA_DIR =      path.join(CLIENT_DIR, 'data')
LOGS_DIR =      path.join(DATA_DIR,   'logs')
DATABASE_DIR =  path.join(DATA_DIR,   'database')
MODEL_DIR =     path.join(DATA_DIR,   'model')
VOICE_DIR =     path.join(DATA_DIR,   'voices')

LOG_NAME = 'myAI'
LOG_FILE = path.join(LOGS_DIR, LOG_NAME+'.log')
LOG_LEVEL = logging.DEBUG

DATABASE_FILE = path.join(DATABASE_DIR, 'database.sql')

API_DIRS = [
    # Add your custom api directory strings here (e.g. - "C:/my_custom_api_dir")
]
API_DIRS.extend(api_library.__path__)
MOD_DIRS = [
    # Add your custom api directory strings here (e.g. - "C:/my_custom_mod_dir")
]
MOD_DIRS.extend(active_mods.__path__)

#DIRS = [LOGS_DIR, MEDIA_DIR, INPUTS_DIR, RESPONSES_DIR, USERS_DIR]
DIRS = [DATA_DIR, LOGS_DIR, DATABASE_DIR, VOICE_DIR]

for d in DIRS:
    if not path.exists(d):
        mkdir(d)


#####################
#     RESPONSES     #
#####################
ERROR =      "I am not able to help you with that"
NO_MODULES = "I'm not sure how to respond to that."
NO_MIC =     "I couldn't connect to a microphone."

#####################
#       KEYS        #
#####################
WOLFRAM_KEY =      'KEY'
WOLFRAM_UNITS =    'metric'

WUNDERGROUND_KEY = 'KEY'

IFTTT_KEY =        'KEY'

#####################
#   BASIC REGEX     #
#####################
PHONE_REGEX = r"\b((\(\d{3}\)|\d{3})-?\d{3}-?\d{4})\s?(.*)"

#####################
#       MQTT        #
#####################
MQTT_SERVER = '10.0.1.22'
MQTT_PORT = 1883

#####################
#       App         #
#####################
SERVER_STARTTIME = ''
REQUESTS_COUNT = 0
ERROR_COUNT = 0