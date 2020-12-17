class Command:

    def __init__(self):
        self.description = "A default command description :("
        self.usage = "<command>"
        self.parser = None
        self.is_prompt_command = False

    def shutdown(self):
        pass

    def help(self):
        print(f"Usage: {self.usage}\nPrompt gadget: {self.is_prompt_command}")

    def execute(self, args):
        if self.is_prompt_command:
            print("This command is only used in your prompt")
        else:
            print("You ran a default command!")

    def execute_prompt(self):
        pass

class CommandInput:

    def __init__(self):
        self.raw_text = None
        self.args = None