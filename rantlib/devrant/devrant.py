####################################
#
#   devRant library
#
####################################

# Imports
import json
import requests

HTTP_OK = 200
HTTP_BAD_REQUEST = 400

class Image:

    def __init__(self):
        self.url = None
        self.width = None
        self.height = None

    def data(self, data):
        self.url = data["url"]
        self.width = data["width"]
        self.height = data["height"]

class ProfileImage:

    def __init__(self):
        self.background_color = None # More descriptive than "b"
        self.image_url = None # More descriptive than "i"

    def data(self, data):
        self.background_color = data["b"]
        self.image_url = data.get("i", None)

# Data object for a user
class User:

    def __init__(self):
        self.username = None
        self.score = None
        self.about = None
        self.location = None
        self.id = None
        self.created_time = None
        self.skills = None
        self.github = None
        self.website = None
        self.content = {"rants": None, "upvoted": None, "comments": None, "favorites": None}
        self.counts = {"rants": None, "upvoted": None, "comments": None, "favorites": None, "collabs": None}
        self.dpp = None
        self.avatar = None
        self.avatar_sm = None

    def data(self, data):
        self.username = data["username"]
        self.score = data["score"]
        self.about = data["about"]
        self.location = data["location"]
        self.id = data["id"]
        self.created_time = data["created_time"]
        self.skills = data["skills"]
        self.github = data["github"]
        self.website = data["website"]
        self.content["rants"] = data["content"]["rants"]
        self.content["upvoted"] = data["content"]["upvoted"]
        self.content["comments"] = data["content"]["comments"]
        self.content["favorites"] = data["content"]["favorites"]
        self.counts["rants"] = data["counts"]["rants"]
        self.counts["upvoted"] = data["counts"]["upvoted"]
        self.counts["comments"] = data["counts"]["comments"]
        self.counts["favorites"] = data["counts"]["favorites"]
        self.dpp = data["dpp"]
        self.avatar = ProfileImage()
        self.avatar.data(data["avatar"])
        self.avatar_sm = ProfileImage()
        self.avatar_sm.data(data["avatar_sm"])

# Data object for a rant
class Rant:

    def __init__(self):
        self.id = None
        self.text = None
        self.score = None
        self.created_time = None
        self.attached_image = None
        self.num_comments = None
        self.tags = None
        self.vote_state = None
        self.user_avatar = None
        self.user = None
        self.user_avatar_lg = None
        self.user_dpp = None

    def data(self, data):
        self.id = data["id"]
        self.text = data["text"]
        self.score = data["score"]
        self.created_time = data["created_time"]
        self.attached_image = Image()
        if data["attached_image"] != "":
            self.attached_image.data(data["attached_image"])
        self.num_comments = data["num_comments"]
        self.tags = data["tags"]
        self.vote_state = data["vote_state"]
        self.user = User()
        self.user.id = data["user_id"]
        self.user.username = data["user_username"]
        self.user.score = data["user_score"]
        self.user_avatar = ProfileImage()
        self.user_avatar.data(data["user_avatar"])
        self.user_avatar_lg = ProfileImage()
        self.user_avatar_lg.data(data["user_avatar_lg"])
        self.user_dpp = data.get("user_dpp", False)

# Data object for a comment
class Comment:

    def __init__(self):
        self.id = None

APP_VERSION = "3"
BASE_URL  = "https://devrant.com/api"
USER_ID_URL = BASE_URL + "/get-user-id"
USERS_URL = BASE_URL + "/users"
LOGIN_URL = USERS_URL + "/auth-token"
DEVRANT_URL = BASE_URL + "/devrant"
RANTS_URL = DEVRANT_URL + "/rants"
RANDOM_RANT_URL = RANTS_URL + "/surprise"
COLLABS_URL = DEVRANT_URL + "/collabs"

def username_to_user_id(username):
    url = f"{USER_ID_URL}?app={APP_VERSION}&username={username}"
    return requests.get(url).json()

def get_user(user_id):
    url = f"{USERS_URL}/{user_id}?app={APP_VERSION}&content=all"
    user = User()
    user.data(requests.get(url).json())
    return user

def login(username, password):
    data = requests.post(LOGIN_URL, data={"username": username, "password": password})
    status_code = data.status_code
    if status_code != HTTP_OK:
        raise data.get("error")
    else:
        return data