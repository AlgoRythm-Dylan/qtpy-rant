####################################
#
#   devRant library
#
####################################

# Imports
import json
import requests


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
        self.image_url = data["i"]

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
        self.user_id = None
        self.user_username = None
        self.user_score = None
        self.user_avatar = None
        self.user_avatar_lg = None
        self.user_dpp = None

    def data(self, data):
        self.id = data["id"]
        self.text = data["text"]
        self.score = data["score"]
        self.created_time = data["created_time"]
        self.attached_image = Image()
        self.attached_image.data(data["attached_image"])
        self.num_comments = data["num_comments"]
        self.tags = data["tags"]
        self.vote_state = data["vote_state"]
        self.user_id = data["user_id"]
        self.user_username = data["user_username"]
        self.user_score = data["user_score"]
        self.user_avatar = profileImage()
        self.user_avatar.data(data["user_avatar"])
        self.user_avatar_lg = profileImage()
        self.user_avatar_lg.data(data["user_avatar_lg"])
        self.user_dpp = data["user_dpp"]

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

class RantGetter:

    def __init__(self):
        self.skip = 0
        self.stride = 50
        self.sort = "algo" # algo, top, recent
        self.time_range = "day" # day, week, month, all
        self.token_id = None
        self.token_key = None
        self.user_id = None

    def get(amount=self.stride, mode=self.mode):
        url = f"{RANTS_URL}?app={APP_VERSION}&sort={mode}&range={self.time_range}&limit={amount}&skip={self.skip}"
        if self.token_id != None:
            url += f"&token_id={self.token_id}&token_key={self.token_key}&user_id={self.user_id}"
        self.skip += amount
        data = requests.get(url).json()
        rants = []
        for rant_data in data["rants"]:
            rant = Rant()
            rant.data(rant_data)
        return rants