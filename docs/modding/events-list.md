# A List of all events
Events are useful for modders, but can be used by the
application too.

## CommandShutdownEvent
Executes before a command is shutdown.
If cancelled, the command is not shut down

Members: `command`

## CommandPostShutdownEvent
Executes after a command is shutdown

Extends `CommandShutdownEvent`

*Note: Not cancellable*

## CommandExecuteEvent
Executes before a command is executed.
If cancelled, the command is not executed

Members: `executor`, `arguments`, `command_text`

## CommandExecutedEvent
Executes after a command is executed

Members: `error`

Extends `CommandExecuteEvent`

*Note: Not cancellable*

## CommandRegisterEvent
Executes before a command is registered.
If cancelled, the command is not registered.
name, executor, alias, and overwrite can be modified

Members: `name`, `executor`, `alias`, `overwrite`

## CommandRegisteredEvent
Executes after a command is registered

Members: `error`

Extends `CommandRegisterEvent`

*Note: Not cancellable*