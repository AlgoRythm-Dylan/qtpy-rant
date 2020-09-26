####################################
#
#   devRant library
#
####################################

# Imports
import json
import requests

# Data object for a rant
class Rant:

    def __init__(self):
        self.id = None


# Data object for a user
class User:

    def __init__(self):
        self.id = None

# Data object for a comment
class Comment:

    def __init__(self):
        self.id = None

APP_VERSION = "3"
BASE_URL  = "https://devrant.com/api"
USERS_URL = BASE_URL + "/users"
LOGIN_URL = USERS_URL + "/auth-token"
DEVRANT_URL = BASE_URL + "/devrant"
RANTS_URL = DEVRANT_URL + "/rants"
RANDOM_RANT_URL = RANTS_URL + "/surprise"
COLLABS_URL = DEVRANT_URL + "/collabs"