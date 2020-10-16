class ReloadCommand:

    def __init__(self, client):
        self.description = "This reload command reloads other commands!"
        self.usage = "reload <command>"

    def execute(self, args):
        pass

def register(client):
    client.register_command("reload", ReloadCommand(client))