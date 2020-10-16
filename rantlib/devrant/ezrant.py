from rantlib.devrant.devrant import *

class RantGetter:

    def __init__(self):
        self.skip = 0
        self.stride = 50
        self.sort = "algo" # algo, top, recent
        self.time_range = "day" # day, week, month, all
        self.token_id = None
        self.token_key = None
        self.user_id = None

    def get(self, amount=None, mode=None):
        if amount == None:
            amount = self.stride
        if mode == None:
            mode = self.sort
        url = f"{RANTS_URL}?app={APP_VERSION}&sort={mode}&range={self.time_range}&limit={amount}&skip={self.skip}"
        if self.token_id != None:
            url += f"&token_id={self.token_id}&token_key={self.token_key}&user_id={self.user_id}"
        self.skip += amount
        data = requests.get(url).json()
        rants = []
        for rant_data in data["rants"]:
            rant = Rant()
            rant.data(rant_data)
            rants.append(rant)
        return rants