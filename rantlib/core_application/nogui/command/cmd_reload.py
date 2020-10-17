from rantlib.core_application.nogui.command.command import Command

class ReloadCommand(Command):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.description = "This reload command reloads other commands"
        self.usage = "reload <command>"

    def execute(self, args):
        args = args.args
        if len(args) == 1:
            command_to_reload = args[0]
            self.client.reload_command(command_to_reload)
        else:
            Command.help(self)
        print("Command reloaded")

    def help(self):
        Command.help(self)
        print("This command reloads other commands but changes on disk will not reflect")

def register(client):
    client.register_command("reload", ReloadCommand(client))