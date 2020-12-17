####################################
#
#   devRant library
#
####################################

if __name__ == "__main__":
    import sys
    import os
    from pathlib import Path
    sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.parent))

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
    def get_rant(rant_id):
        return RantAPI.generic_request(f"{RANTS_URL}/{rant_id}")

    @staticmethod
    def get_user_id(username):
        data = RantAPI.generic_request(f"{USER_ID_URL}", params={"username": username})
        return data["user_id"]

    @staticmethod
    def get_user(user_id, content="collabs"):
        data = RantAPI.generic_request(f"{USERS_URL}/{user_id}", params={"content": content})
        return data["profile"]

    @staticmethod
    def login(username, password):
        return RantAPI.generic_request(f"{LOGIN_URL}", data={"username": username, "password": password})

    @staticmethod
    def rant_feed(mode="algo",
                  time_range="day",
                  limit=50,
                  skip=0,
                  token_id=None,
                  token_key=None,
                  user_id=None):
        request_data = {
            "sort": mode,
            "range": time_range,
            "limit": limit,
            "skip": skip
        }
        if token_id != None:
            request_data["token_id"] = token_id
            request_data["token_key"] = token_key
            request_data["user_id"] = user_id
        return RantAPI.generic_request(f"{RANTS_URL}", data=request_data)["rants"]


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
        super().__init__()
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
        super().__init__()
        self.import_fields = {
            "id": int,
            "rant_id": int,
            "body": str,
            "score": int,
            "created_time": int,
            "vote_state": int,
            "user": User(),
            "attached_image": Image()
        }
        self.init_fields()

    def has_image(self):
        return self.attached_image != None and self.attached_image.url != None
    
    def __str__(self):
        return self.body

class Rant(DataClass):

    def __init__(self):
        super().__init__()
        self.import_fields = {
            "id": int,
            "text": str,
            "score": int,
            "created_time": int,
            "attached_image": Image(),
            "num_comments": int,
            "comments": object,
            "tags": object,
            "vote_state": int,
            "user_avatar": ProfileImage(),
            "user_avatar_lg": ProfileImage(),
            "user": User(),
            "user_dpp": bool
        }
        self.init_fields()

    def has_image(self):
        return self.attached_image != None and self.attached_image.url != None

    def comments_loaded(self):
        return self.comments != None and len(self.comments) == self.num_comments

    def load(self):
        data = RantAPI.get_rant(self.id)
        import_data = data.get("rant")
        import_data["comments"] = data.get("comments")
        self.import_data(import_data)

    def after_data_import(self, data):
        if data.get("user_username") != None:
            self.user.id = data.get("user_id")
            self.user.username = data.get("user_username")
            self.user.score = data.get("user_score")
        # Convert "raw" data dict to objective class
        if type(self.comments) == list and len(self.comments) != 0 and not isinstance(self.comments[0], Comment):
            objective_comments = []
            for comment in self.comments:
                obj_comment = Comment()
                obj_comment.import_data(comment)
                obj_comment.user.id = comment.get("user_id")
                obj_comment.user.username = comment.get("user_username")
                obj_comment.user.score = comment.get("user_score")
                objective_comments.append(obj_comment)
            self.comments = objective_comments

    def __str__(self):
        return self.text

class RantLib:

    @staticmethod
    def get_rant(rant_id):
        data = RantAPI.get_rant(rant_id)
        import_data = data.get("rant")
        import_data["comments"] = data.get("comments")
        rant = Rant()
        rant.import_data(import_data)
        return rant

    @staticmethod
    def get_user(user_id):
        data = RantAPI.get_user(user_id)
        user = User()
        user.import_data(data)
        return user

    @staticmethod
    def rant_feed(mode="algo",
            time_range="day",
            limit=50,
            skip=0,
            token_id=None,
            token_key=None,
            user_id=None):
        rants = RantAPI.rant_feed(
            mode=mode,
            time_range=time_range,
            limit=limit,
            skip=skip,
            token_id=token_id,
            token_key=token_key,
            user_id=user_id)
        objective_rants = []
        for rant in rants:
            obj_rant = Rant()
            obj_rant.import_data(rant)
            objective_rants.append(obj_rant)
        return objective_rants
        

""" 
    
def get_notifs(user_id, token_id, token_key):
    pass

def get_feed(user_id, token_id, token_key):
    url = f"{FEED_URL}?app={APP_VERSION}&user_id={user_id}&token_id={token_id}&token_key={token_key}"
    req = requests.get(url)
    
"""

if __name__ == "__main__":
    #print(RantLib.get_rant(3744668).comments)
    #print(RantAPI.get_user(RantAPI.get_user_id("AlgoRythm")))
    #print(RantLib.get_user(RantAPI.get_user_id("AlgoRythm")).avatar)
    print(RantLib.rant_feed())