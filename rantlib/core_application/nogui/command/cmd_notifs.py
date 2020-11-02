from rantlib.core_application.nogui.command.command import Command

class NotifsCommand(Command):

    def __init__(self, client):
        super().__init__()
        self.description = "Read your notifications"
        self.usage = "notifs"
        self.is_prompt_command = True

    def help(self):
        Command.help(self)

    def execute(self, args):
        print("You have no notifications, lonely ass")

    def execute_prompt(self):
        print("", end="")

def register(client):
    client.register_command("notifs", NotifsCommand(client))