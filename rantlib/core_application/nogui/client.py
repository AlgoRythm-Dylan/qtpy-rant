####################################
#
#   non-graphical main entrypoint
#
####################################

import sys
from os import walk
from pathlib import Path
from importlib import import_module

from rantlib.core_application.client import Client

class TerminalDevRantClient(Client):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.commands = {}
        self.aliases = {}
        self.prompt_text = "\\u >> "
        self.import_commands()

    def do_login_flow(self):
        print("Auth not implemented yet. Check in later.")

    def get_prompt(self):
        # Do some simple string replacements on prompt
        prompt = self.prompt_text
        prompt = prompt.replace("\\u", "Guest" if self.qtpy.is_guest_mode() else self.qtpy.current_user.username)
        return prompt

    def register_command(self, name, executor, alias=None, overwrite=False):
        insert = name not in self.commands or overwrite
        if insert:
            self.commands[name] = executor

    def import_commands(self):
        commands_path = Path(__file__).parent.joinpath("command")
        for dirpath, dirnames, filenames in walk(commands_path):
            for file in filenames:
                if file.startswith("cmd_"):
                    imported_module = import_module(f"rantlib.core_application.nogui.command.{file[:file.find('.py')]}")
                    imported_module.register(self)
            break

    def run(self):
        self.do_login_flow()
        print("Running in CLI mode. Type \"exit\" to quit")
        while True:
            raw_command_text = input(self.get_prompt())
            if raw_command_text == "exit": # Exit hard quit
                sys.exit(0)
            elif raw_command_text == "":
                continue
            next_space = raw_command_text.find(" ")
            if next_space == -1:
                command = raw_command_text
            else:
                raw_command_text[:next_space]
            if command in self.commands:
                print("Command run")
            elif command in self.aliases:
                print("Alias for command run")
            else:
                print(f"Unknown command: {command}")