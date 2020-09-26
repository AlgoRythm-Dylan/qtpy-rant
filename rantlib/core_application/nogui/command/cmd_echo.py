from rantlib.core_application.nogui.command.command import Command

class EchoCommand(Command):

    def __init__(self):
        super().__init__()
        self.description = "The sanity check command. Repeats whatever you tell it"
        self.usage = "<command> <arguments>"

def register(client):
    client.register_command("echo", EchoCommand())