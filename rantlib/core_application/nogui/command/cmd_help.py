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
                help_text = f"- {command_name}:\n\t{command.description}\n"
                help_text += f"\t{self.client.qtpy.language.get('cli_hint_usage')}: {command.usage}\n"
                help_text += f"\tPrompt gadget: {command.is_prompt_command}"
                print(help_text)
        else:
            command = self.client.get_command_by_name(args.args[0])
            if command != None:
                command.help()
            else:
                print(self.client.qtpy.language.get("cli_unknown_command"))

    def help(self):
        Command.help(self)
        print("This is the help command. You can call it with no arguments to get a description of all commands.")
        print("You can also pass a command as an argument to get more detailed help, if the command provides it.")

def register(client):
    client.register_command("help", HelpCommand(client), "?")