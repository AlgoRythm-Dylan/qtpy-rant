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
        self.import_commands()

    def register_command(self, name, executor, aliases=[], overwrite=False):
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
        while True:
            raw_command_text = input(">> ")
            if raw_command_text == "exit":
                sys.exit(0)