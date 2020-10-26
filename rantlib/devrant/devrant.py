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

class Auth:

    def __init__(self):
        self.id = None
        self.key = None
        self.expire_time = None
        self.username = None

    def data(self, data):
        auth = data["auth_token"]
        self.id = auth["id"]
        self.key = auth["key"]
        self.expire_time = auth["expire_time"]
        self.user_id = auth["user_id"]

    def update_username(self):
        user = User()
        user.id = self.id
        user.load()
        self.username = user.username

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
        self.auth = None

    def data(self, data):
        profile = data["profile"]
        self.username = profile.get("username")
        self.score = profile.get("score")
        self.about = profile.get("about")
        self.location = profile.get("location")
        self.created_time = profile.get("created_time")
        self.skills = profile.get("skills")
        self.github = profile.get("github")
        self.website = profile.get("website")
        content = profile["content"]["content"]
        self.content["rants"] = content["rants"]
        self.content["upvoted"] = content["upvoted"]
        self.content["comments"] = content["comments"]
        self.content["favorites"] = content["favorites"]
        counts = profile["content"]["counts"]
        self.counts["rants"] = counts["rants"]
        self.counts["upvoted"] = counts["upvoted"]
        self.counts["comments"] = counts["comments"]
        self.counts["favorites"] = counts["favorites"]
        self.dpp = profile.get("dpp")
        self.avatar = ProfileImage()
        self.avatar.data(profile["avatar"])
        self.avatar_sm = ProfileImage()
        self.avatar_sm.data(profile["avatar_sm"])

    def is_dpp(self):
        return self.dpp == True

    def load(self):
        if self.id == None and self.username == None:
            raise Exception("User ID or name required for this operation")
        if self.id == None:
            self.id = username_to_user_id(self.username)
        self.data(get_user(self.id, raw_data=True))



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
        if data["attached_image"] != "":
            self.attached_image = Image()
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

    def has_image(self):
        return self.attached_image != None

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
    request = requests.get(url)
    data = request.json()
    if request.status_code == HTTP_OK:
        return data["user_id"]
    else:
        raise Exception(data.get("error"))

def get_user(user_id, raw_data=False):
    url = f"{USERS_URL}/{user_id}?app={APP_VERSION}&content=all"
    user = User()
    request = requests.get(url)
    data = request.json()
    if request.status_code == HTTP_OK:
        if raw_data:
            return data
        else:
            user = User()
            user.data(data)
            return user
    else:
        raise Exception(data.get("error"))

def login(username, password):
    req = requests.post(f"{LOGIN_URL}?app={APP_VERSION}&username={username}&password={password}")
    status_code = req.status_code
    print(req.request.url)
    data = req.json()
    if status_code != HTTP_OK:
        raise Exception(data.get("error"))
    else:
        auth = Auth()
        auth.data(data)
        auth.update_username()
        return auth