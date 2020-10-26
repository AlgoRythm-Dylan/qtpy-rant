from rantlib.core_application.nogui.util import *
from rantlib.core_application.nogui.command.command import Command

class CommentCommand(Command):

    def __init__(self, client):
        super().__init__()
        self.description = "Read and write comments"
        self.usage = "comment"
        self.client = client

    def execute(self, args):
        rant = None
        comment_index = None
        try:
            rant = self.client.temp_data["rant"]
            comment_index = self.client.temp_data["comment_index"]
        except:
            print("No rant selected")
            return
        comments = rant.get("comments", [])
        box = Box()
        box.add_section(comment.text)
        
def register(client):
    client.register_command("comment",  CommentCommand(client))