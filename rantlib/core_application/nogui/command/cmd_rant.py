from rantlib.core_application.nogui.command.command import Command
from rantlib.devrant.ezrant import RantGetter
from rantlib.core_application.lang import simple_replace
from rantlib.core_application.nogui.util import *
from rantlib.core_application.storage import append_with_max

class RantCommand(Command):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.description = self.client.qtpy.language.get("cli_rant_command_description")
        self.usage = "rant <?next|last|recent-autofeed>"
        self.rant_getter = RantGetter()
        self.rant_getter.stride = 20
        self.rant_buffer = []
        self.read_rants = [] # Read as in "has already been read"
        self.last_rant = None

    def execute(self, args):
        args = args.args
        if len(args) == 0:
            self.display_rant()
        if len(args) == 1:
            if args[0] == "next":
                self.display_rant()
            elif args[0] == "previous" or args[0] == "last":
                if len(self.read_rants) == 0:
                    print("There is no previous rant")
                else:
                    current_rant = self.client.temp_data.get("rant")
                    if current_rant != None:
                        self.rant_buffer.insert(0, current_rant)
                    self.rant_buffer.insert(0, self.read_rants.pop(0))
                    self.display_rant()
            elif args[0] == "recent-autofeed":
                self.recent_autofeed()
                
    def check_rant_buffer(self):
        if len(self.rant_buffer) == 0:
            print("Loading rants...")
            if not self.client.qtpy.is_guest_mode():
                token = self.client.qtpy.auth_service.current_user()
                self.rant_getter.token_id = token.id
                self.rant_getter.token_key = token.key
                self.rant_getter.user_id = token.user_id
            else:
                self.rant_getter.token_id = None
                self.rant_getter.token_key = None
                self.rant_getter.user_id = None
            self.rant_buffer = self.rant_getter.get()

    def display_rant(self):
        self.check_rant_buffer()
        rant = self.rant_buffer.pop(0)
        if self.client.temp_data.get("rant") != None:
            append_with_max(self.read_rants, self.client.temp_data["rant"], 200)
        self.client.temp_data["rant"] = rant
        self.client.temp_data["comment_index"] = 0
        box = Box(self.client.config.get("preferred_width"))
        score_string = f"{self.client.qtpy.language.get('score')}: {rant.score}, "
        score_string += f"{self.client.qtpy.language.get('rant_id')}: {rant.id}"
        box.add_section(two_column(score_string, f"{rant.user.username} ({rant.user.score})", box.inner_space()))
        box.add_section(rant.text)
        if rant.has_image():
            image_str = f"{rant.attached_image.url} ({rant.attached_image.width}x{rant.attached_image.height})"
            box.add_section(f"{self.client.qtpy.language.get('image')}: {image_str}")
        comments_text = f"   {self.client.qtpy.language.get('comments')}: {rant.num_comments}"
        tags = constrain_text(", ".join(rant.tags), box.inner_space() - len(comments_text))
        last_panel = two_column(tags.pop(0), comments_text, box.inner_space()) + "".join(tags)
        box.add_section(last_panel)
        print(box.render(), end="")

    def recent_autofeed(self):
        print("This feed will update with the most recent posts until you quit by sending a Keyboard Interrupt (ctrl/cmd + c)")

    def help(self):
        Command.help(self)
        for line in self.client.qtpy.language.get("cli_rant_command_help_lines"):
            print(line)

def register(client):
    client.register_command("rant", RantCommand(client))