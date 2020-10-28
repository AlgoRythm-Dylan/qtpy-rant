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
        if rant.num_comments == 0:
            print("This rant has no comments")
            return
        if not rant.comments_loaded():
            print("Loading comments...")
            rant.load()
        if comment_index >= rant.num_comments:
            print("You have read all of the comments on this rant")
            return
        print(f"Comment {comment_index + 1} of {rant.num_comments}")
        comment = rant.comments[comment_index]
        self.client.temp_data["comment_index"] += 1
        box = Box(self.client.config.get("preferred_width"))
        col1 = f"{self.client.qtpy.language.get('score')}: {comment.score}"
        col2 = f"{comment.user.username} ({comment.user.score})"
        box.add_section(two_column(col1, col2, box.inner_space()))
        box.add_section(comment.body)
        if comment.has_image():
            image = comment.attached_image
            image_lang = self.client.qtpy.language.get('image')
            box.add_section(f"{image_lang}: {image.url} ({image.width}x{image.height})")
        print(box.render())
        
def register(client):
    client.register_command("comment",  CommentCommand(client))