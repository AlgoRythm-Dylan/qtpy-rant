from rantlib.app.cli.command.command import Command

class EchoCommand(Command):

    def __init__(self):
        super().__init__()
        self.description = "The sanity check command. Repeats whatever you tell it"
        self.usage = "echo <?arguments>"

    def execute(self, args):
        print(" ".join(args.args))

def register(client):
    client.register_command("echo", EchoCommand())