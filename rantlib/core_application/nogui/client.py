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
from rantlib.core_application.event.command import *
from rantlib.core_application.nogui.prompt import Prompt


def generic_error_thrower(message):
    raise Exception(message)

class TerminalClient(Client):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.version = "0.1.0"
        self.commands = {}
        self.aliases = {}
        self.config = TerminalConfig()
        self.config.read_data_file(STD_PATH_CLI_CONFIG)
        self.prompt = Prompt(self, src=self.config.get("prompt"))
        self.command_count = 0
        self.import_commands()

    def do_login_flow(self):
        if len(self.qtpy.auth_service.users) == 0:
            print(self.qtpy.language.get("cli_no_users_logged_in"))
            answer = input(f"[{self.qtpy.language.get('cli_confirm_positive')}/{self.qtpy.language.get('cli_confirm_negative')}]: ").upper()
            if answer == self.qtpy.language.get('cli_confirm_positive').upper():
                print(self.qtpy.language.get("warning"))
                print(self.qtpy.language.get("third_party_warning"))
                while(self.qtpy.auth_service.current_user() == None):
                    username = input(f"{self.qtpy.language.get('username')}: ")
                    if username == "":
                        return
                    password = getpass(f"{self.qtpy.language.get('password')}: ")
                    try:
                        self.qtpy.login(username, password)
                    except Exception as e:
                        print(self.qtpy.language.get("login_failure"))
                        print(e)
                        print(self.qtpy.language.get("cli_login_cancel_instructions"))
            else:
                print(self.qtpy.language.get("cli_continuing_as_guest"))

    def register_command(self, name, executor, alias=None, overwrite=False):
        command_register_event = CommandRegisterEvent(name, executor, alias, overwrite)
        self.qtpy.dispatch("register_command", command_register_event)
        if command_register_event.cancelled:
            return
        name = command_register_event.name
        executor = command_register_event.executor
        alias = command_register_event.alias
        overwrite = command_register_event.overwrite

        insert = name not in self.commands or overwrite
        if insert:
            self.commands[name] = executor
        if type(alias) == str:
            pass
        elif type(alias) == list:
            pass
        if executor.parser:
            executor.parser.error = generic_error_thrower

        command_registered_event = CommandRegisteredEvent(name, executor, alias, overwrite)
        self.qtpy.dispatch("command_registered", command_registered_event)

    def import_commands(self):
        commands_path = Path(__file__).parent.joinpath("command")
        for dirpath, dirnames, filenames in walk(commands_path):
            for file in filenames:
                if file.startswith("cmd_"):
                    self.import_module(f"rantlib.core_application.nogui.command.{file[:file.find('.py')]}")
            break

    def run(self):
        self.do_login_flow()
        while True:
            self.command_count += 1
            self.prompt.compile(self.config.get("prompt"))
            self.prompt.print()
            raw_command_text = input()
            self.execute_text(raw_command_text)

    def reload_command(self, command_text):
        # call shutdown
        command = self.commands.get(command_text)
        if command == None:
            return
        shutdown_event = CommandShutdownEvent(command)
        self.qtpy.dispatch("command_shutdown", shutdown_event)
        if shutdown_event.cancelled:
            return
        shutdown_error = None
        try:
            command.shutdown()
        except Exception as e:
            shutdown_error = e
            print(f"Command did not shutdown correctly and may misbehave: {e}")
        post_shutdown_event = CommandPostShutdownEvent(command, error=shutdown_error)
        self.qtpy.dispatch("command_post_shutdown", post_shutdown_event)
        # Clear out the executor from aliases and commands dict
        del self.commands[command_text]
        # re-import with .__module__
        self.import_module(command.__module__)

    def import_module(self, modstr):
        try:
            imported_module = import_module(modstr)
            imported_module.register(self)
        except Exception as e:
            print(f"Could not import module {modstr}: {e}")
    
    def execute_text(self, raw_command_text):
        if raw_command_text == self.qtpy.language.get("cli_exit"):
                sys.exit(0)
        elif raw_command_text == "":
            return
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
                    return
            execute_event = CommandExecuteEvent(executor, command_input, raw_command_text)
            self.qtpy.dispatch("command_execute", execute_event)
            if execute_event.cancelled:
                return
            command_error = None
            try:
                executor.execute(command_input)
            except Exception as e:
                print(f"{self.qtpy.language.get('cli_command_failure')}: \n{e}", file=sys.stderr)
                command_error = e
            executed_event = CommandExecutedEvent(executor, command_input, raw_command_text, error=command_error)
            self.qtpy.dispatch("command_executed", executed_event)