from rantlib.core_application.nogui.command.command import Command
from rantlib.devrant.ezrant import RantGetter
from rantlib.core_application.lang import simple_replace
from rantlib.core_application.nogui.util import *

class RantCommand(Command):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.description = self.client.qtpy.language.get("cli_rant_command_description")
        self.usage = "rant <?next|open>"
        self.rant_getter = RantGetter()
        self.rant_getter.stride = 20
        self.rant_buffer = []
        self.last_rant = None

    def execute(self, args):
        if len(self.rant_buffer) == 0:
            self.rant_buffer = self.rant_getter.get()
        rant = self.rant_buffer.pop()
        self.last_rant = rant
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

    def help(self):
        Command.help(self)
        for line in self.client.qtpy.language.get("cli_rant_command_help_lines"):
            print(line)

def register(client):
    client.register_command("rant", RantCommand(client))