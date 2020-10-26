from rantlib.core_application.nogui.command.command import Command
from rantlib.core_application.storage import STD_PATH_CLI_CONFIG

class SetCommand(Command):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.description = "The settings command"
        self.usage = "set ?(<key>|<key> <value>|--remove <key>|--restore <key>)"

    def execute(self, args):
        if len(args.args) == 0:
            # Print config file path
            print("Config file path (may not exist until changes are made): " + STD_PATH_CLI_CONFIG)
            # Print a list from the config
            for key, value in self.client.config.values.items():
                print(f"Item: {key}\n\tValue: {value}\n\tType: {type(value).__name__}")
        elif len(args.args) == 1:
            key = args.args[0]
            value = self.client.config.values[key]
            print(f"Item: {key}\n\tValue: {value}\n\tType: {type(value).__name__}")
        elif len(args.args) >= 2:
            if args.args[0] == "--remove":
                self.client.config.remove(args.args[1])
            elif args.args[0] == "--restore":
                self.client.config.restore_default(args.args[1]) 
            else:
                key = args.args.pop(0)
                value = " ".join(args.args)
                self.client.config.set(key, parse_type(value))
            self.client.config.write_data_file(STD_PATH_CLI_CONFIG)
        else:
            raise Exception(f"Invalid number of arguments ({len(args.args)})")

    def help(self):
        Command.help(self)
        print("This is the set command, which allows you to modify CLI client settings")
        print("This command only works for simple types: int, float, and str")
        print("Beware that setting something incorrectly may cause instability and crashes\n")
        print("You can call the command without arguments to get a list of settings")
        print("You can call the command with one argument to get the value of that key")
        print("You can call the command with the --remove option to remove a key")
        print("\tNote: keys with defaults will repopulate after restart")
        print("To restore a key to its default (if it has one), use the --restore option")

# Braindead simple bullshit
def parse_type(arg):
    if arg == "None":
        return None
    try:
        int(arg)
        if arg.find(".") != -1:
            return float(arg)
        else:
            return int(arg)
    except:
        return arg

def register(client):
    client.register_command("set", SetCommand(client))