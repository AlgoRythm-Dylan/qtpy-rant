from rantlib.core_application.nogui.command.command import Command
from argparse import ArgumentParser

class HelpCommand(Command):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.description = "Help command"
        self.usage = "help <?command>"

    def execute(self, args):
        if len(args.args) == 0:
            print(self.client.qtpy.language.get("cli_hint_exit"))
            commands = sorted(self.client.commands.keys())
            for command_name in commands:
                command = self.client.commands.get(command_name)
                print(f"- {command_name}:\n\t{command.description}\n\t{self.client.qtpy.language.get('cli_hint_usage')}: {command.usage}")
        else:
            command = self.client.commands.get(args.args[0], None)
            if command != None:
                command.help()
            else:
                print(self.client.qtpy.language.get("cli_unknown_command"))

    def help(self):
        print("This is the help command. You can call it with no arguments to get a description of all commands.")
        print("You can also pass a command as an argument to get more detailed help, if the command provides it.")

def register(client):
    client.register_command("help", HelpCommand(client))