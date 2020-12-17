####################################
#
#   devRant library
#
####################################

if __name__ == "__main__":
    import sys
    sys.path.append("C:\\Users\\Dylan\\Projects\\qtpy-rant")

# Imports
import json
import requests

from rantlib.core_application.storage import DataClass

APP_VERSION = "3"
BASE_URL  = "https://devrant.com/api"
USER_ID_URL = BASE_URL + "/get-user-id"
USERS_URL = BASE_URL + "/users"
ME_URL = BASE_URL + "/me"
FEED_URL = ME_URL + "/feed"
LOGIN_URL = USERS_URL + "/auth-token"
DEVRANT_URL = BASE_URL + "/devrant"
RANTS_URL = DEVRANT_URL + "/rants"
RANDOM_RANT_URL = RANTS_URL + "/surprise"
COLLABS_URL = DEVRANT_URL + "/collabs"

class RantAPIException(Exception):
    """Exception raised when an error is returned by the devRant REST API"""

class RantAPI:

    @staticmethod
    def generic_request(url, params={}, data={}, method="GET"):
        if params.get("app") == None:
            params["app"] = APP_VERSION
        response = requests.request(method,
                                    url,
                                    params=params,
                                    data=data).json()
        if response.get("success") == False:
            raise RantAPIException(response.get("error"))
        else:
            return response

    @staticmethod
    def get_rant(id):
        return RantAPI.generic_request(f"{RANTS_URL}/{id}")

class Image(DataClass):

    def __init__(self):
        super().__init__()
        self.import_fields = {
            "url": str,
            "width": int,
            "height": int
        }
        self.init_fields()

class ProfileImage(DataClass):

    def __init__(self):
        super().__init__()
        self.import_fields = {
            "b": str,
            "i": str
        }
        self.translate_fields = {
            "b" : "background_color",
            "i": "image_url"
        }
        self.init_fields()

class Auth(DataClass):

    def __init__(self):
        super().__init__()
        self.import_fields = {
            "id": int,
            "user_id": int,
            "key": str,
            "expire_time": int,
            "username": str
        }
        self.init_fields()

    def update_username(self):
        user = User()
        user.id = self.user_id
        user.load()
        self.username = user.username

class User(DataClass):

    def __init__(self):
        self.import_fields = {
            "username": str,
            "score": int,
            "about": str,
            "location": str,
            "id": int,
            "created_time": int,
            "skills": str,
            "github": str,
            "website": str,
            "content": object,
            "counts": object,
            "dpp": bool,
            "avatar": ProfileImage(),
            "avatar_sm": ProfileImage(),
            "auth": None
        }
        self.init_fields()

class Comment(DataClass):

    def __init__(self):
        self.import_fields = {
            "id": int,
            "rant_id": int,
            "body": str,
            "score": int,
            "created_time": int,
            "vote_state": int,
            "user": object,
            "attached_image": Image()
        }

    def has_image(self):
        return self.attached_image != None

    def to_string(self):
        return self.body

class Rant(DataClass):

    def __init__(self):
        super().__init__()
        self.import_fields = {
            "id": int,
            "text": str,
            "score": int
        }

class RantLib:
"""Objective rant library"""

    @staticmethod
    def get_rant(id):
        data = RantAPI.get_rant(id).get("rant")
        rant = Rant()
        rant.import_data(data)
        return rant

""" 

# Data object for a rant
class Rant:

    def __init__(self):
        self.id = None
        self.text = None
        self.score = None
        self.created_time = None
        self.attached_image = None
        self.num_comments = None
        self.comments = []
        self.tags = None
        self.vote_state = None
        self.user_avatar = None
        self.user = None
        self.user_avatar_lg = None
        self.user_dpp = None

    def data(self, data):
        rant = data
        if rant.get("id") == None:
            rant = data["rant"] # For loading from rant detail endpoint
        self.id = rant["id"]
        self.text = rant["text"]
        self.score = rant["score"]
        self.created_time = rant["created_time"]
        if rant["attached_image"] != "":
            self.attached_image = Image()
            self.attached_image.data(rant["attached_image"])
        self.num_comments = rant["num_comments"]
        for comment_data in data.get("comments", []):
            comment = Comment()
            comment.data(comment_data)
            self.comments.append(comment)
        self.tags = rant["tags"]
        self.vote_state = rant["vote_state"]
        self.user = User()
        self.user.id = rant["user_id"]
        self.user.username = rant["user_username"]
        self.user.score = rant["user_score"]
        self.user_avatar = ProfileImage()
        self.user_avatar.data(rant["user_avatar"])
        self.user_avatar_lg = ProfileImage()
        self.user_avatar_lg.data(rant["user_avatar_lg"])
        self.user_dpp = rant.get("user_dpp", False)

    def has_image(self):
        return self.attached_image != None

    def comments_loaded(self):
        return len(self.comments) == self.num_comments

    def load(self):
        self.data(get_full_rant(self.id, raw_data=True))

    def to_string(self):
        return self.text

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

def get_full_rant(id, raw_data=False):
    url = f"{RANTS_URL}/{id}?app={APP_VERSION}"
    req = requests.get(url)
    data = req.json()
    if data.get("success") != True:
        raise Exception(data.get("error"))
    if raw_data:
        return data
    else:
        rant = Rant()
        rant.data(data)
        return rant

def login(username, password):
    data = {"app": APP_VERSION, "username": username, "password": password}
    req = requests.post(LOGIN_URL, data=data)
    data = req.json()
    status_code = req.status_code
    if status_code != HTTP_OK:
        raise Exception(data.get("error"))
    else:
        auth = Auth()
        auth.data(data)
        auth.update_username()
        return auth

def get_rants(mode="algo", time_range="day", limit=50, skip=0, token_id=None, token_key=None, user_id=None, raw_data=False):
    url = f"{RANTS_URL}?app={APP_VERSION}&sort={mode}&range={time_range}&limit={limit}&skip={skip}"
    if token_id != None:
        url += f"&token_id={token_id}&token_key={token_key}&user_id={user_id}"
    request = requests.get(url)
    data = request.json()
    success = data.get("success", False)
    if not success:
        raise Exception(data.get("error"))
    if raw_data:
        return data
    rants_data = data.get("rants")
    rants = []
    for rant_data in rants_data:
        rant = Rant()
        rant.data(rant_data)
        rants.append(rant)
    return rants
    
def get_notifs(user_id, token_id, token_key):
    pass

def get_feed(user_id, token_id, token_key):
    url = f"{FEED_URL}?app={APP_VERSION}&user_id={user_id}&token_id={token_id}&token_key={token_key}"
    req = requests.get(url)
    
"""

if __name__ == "__main__":
    print(RantLib.get_rant(3744668).text)