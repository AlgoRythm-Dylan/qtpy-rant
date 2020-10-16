# Command events file
from rantlib.core_application.event.event import Event

# Executes before a command is shutdown
# if cancelled, the command is not shut down
class CommandShutdownEvent(Event):

    def __init__(self, command):
        super().__init__()
        self.command = command

# Executes after a command is shutdown
class CommandPostShutdownEvent(CommandShutdownEvent):

    def __init__(self, command, error=None):
        super().__init__(command)
        self.is_cancellable = False
        self.error = error

# Executes before a command is executed
# if cancelled, the command is not executed
class CommandExecuteEvent(Event):

    def __init__(self, executor, arguments, command_text):
        super().__init__()
        self.executor = executor
        self.arguments = arguments
        self.command_text = command_text

# Executes after a command is executed
class CommandExecutedEvent(CommandExecuteEvent):

    def __init__(self, executor, arguments, command_text, error=None):
        super().__init__(executor, arguments, command_text)
        self.error = error
        self.is_cancellable = False