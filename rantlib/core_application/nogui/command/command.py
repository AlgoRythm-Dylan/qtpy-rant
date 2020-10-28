class Command:

    def __init__(self):
        self.description = "A default command description :("
        self.usage = "<command>"
        self.parser = None
        self.is_prompt_command = False

    def shutdown(self):
        pass

    def help(self):
        print(f"Usage: {self.usage}")

    def execute(self, args):
        print("You ran a default command!")

    def execute_prompt(self):
        pass

class CommandInput:

    def __init__(self):
        self.raw_text = None
        self.args = None