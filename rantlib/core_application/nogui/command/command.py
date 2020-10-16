class Command:

    def __init__(self):
        self.description = "A default command description :("
        self.usage = "<command>"
        self.parser = None

    def help(self):
        print(f"Usage: {self.usage}")

    def execute(self, args):
        print("You ran a default command!")

class CommandInput:

    def __init__(self):
        self.raw_text = None
        self.args = None