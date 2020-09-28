from rantlib.core_application.nogui.command.command import Command

class RantCommand(Command):

    def __init__(self):
        super().__init__()
        self.description = "The rant command"

def register(client):
    client.register_command("rant", RantCommand())