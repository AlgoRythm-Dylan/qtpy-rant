####################################
#
#   non-graphical main entrypoint
#
####################################

import sys
from os import walk
from pathlib import Path
from importlib import import_module
from getpass import getpass

from rantlib.core_application.client import Client
from rantlib.core_application.nogui.command.command import CommandInput
from rantlib.core_application.nogui.config import TerminalConfig
from rantlib.core_application.storage import STD_PATH_CLI_CONFIG

def generic_error_thrower(message):
    raise Exception(message)

class TerminalClient(Client):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.commands = {}
        self.aliases = {}
        self.config = TerminalConfig()
        self.config.read_data_file(STD_PATH_CLI_CONFIG)
        self.import_commands()

    def do_login_flow(self):
        if len(self.qtpy.auth_service.users) == 0:
            print(self.qtpy.language.get("cli_no_users_logged_in"))
            answer = input(f"[{self.qtpy.language.get('cli_confirm_positive')}/{self.qtpy.language.get('cli_confirm_negative')}]: ").upper()
            if answer == self.qtpy.language.get('cli_confirm_positive').upper():
                print(self.qtpy.language.get("warning"))
                print(self.qtpy.language.get("third_party_warning"))
                username = input(f"{self.qtpy.language.get('username')}: ")
                password = getpass(f"{self.qtpy.language.get('password')}: ")
                print(username, password)
            else:
                print(self.qtpy.language.get("cli_continuing_as_guest"))

    def get_prompt(self):
        # Do some simple string replacements on prompt
        prompt = self.config.get("prompt")
        prompt = prompt.replace("\\u", self.qtpy.language.get("guest") if self.qtpy.is_guest_mode() else self.qtpy.current_user.username)
        return prompt

    def register_command(self, name, executor, alias=None, overwrite=False):
        insert = name not in self.commands or overwrite
        if insert:
            self.commands[name] = executor
        if type(alias) == str:
            pass
        elif type(alias) == list:
            pass
        if executor.parser:
            executor.parser.error = generic_error_thrower

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
        while True:
            raw_command_text = input(self.get_prompt())
            if raw_command_text == self.qtpy.language.get("cli_exit"):
                sys.exit(0)
            elif raw_command_text == "":
                continue
            next_space = raw_command_text.find(" ")
            if next_space == -1:
                command = raw_command_text
            else:
                command = raw_command_text[:next_space]
            command_input = CommandInput()
            command_input.raw_text = raw_command_text
            executor = None
            if command in self.commands:
                executor = self.commands[command]
            elif command in self.aliases:
                executor = self.aliases[command]
            if executor == None:
                print(f"{self.qtpy.language.get('cli_unknown_command')}: {command}")
            else:
                arg_string = raw_command_text[len(command) + 1:]
                if executor.parser == None:
                    if len(arg_string) == 0:
                        command_input.args = []
                    else:
                        command_input.args = arg_string.split(" ")
                else:
                    try:
                        command_input.args = executor.parser.parse_args(arg_string)
                    except Exception as e:
                        print(f"{self.qtpy.language.get('cli_command_failure')}: {e}", file=sys.stderr)
                        continue
                try:
                    executor.execute(command_input)
                except Exception as e:
                    print(f"{self.qtpy.language.get('cli_command_failure')}: \n{e}", file=sys.stderr)