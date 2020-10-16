from rantlib.core_application.nogui.command.command import Command
from rantlib.devrant.ezrant import RantGetter
from rantlib.core_application.lang import simple_replace

class RantCommand(Command):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.description = "The rant command"
        self.usage = "rant <?next|open>"
        self.rant_getter = RantGetter()
        self.rant_getter.stride = 20
        self.rant_buffer = []

    def execute(self, args):
        if len(self.rant_buffer) == 0:
            self.rant_buffer = self.rant_getter.get()
        rant = self.rant_buffer.pop()
        rant_label = simple_replace(self.client.qtpy.language.get("cli_rant_label"), {"RANT": rant.id, "USER": rant.user.username})
        print(f"{'-'*10}\n\t{rant_label}\n{'-'*10}\n")
        print(rant.text)

    def help(self):
        print("The rant command")
        print("Execute with no arguments to get a rant")
        print("This has the same effect as executing \"rant next\"")

def register(client):
    client.register_command("rant", RantCommand(client))