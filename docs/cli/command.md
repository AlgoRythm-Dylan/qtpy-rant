# Write a custom command
*Quickstart: create your command in three easy steps*

## 1) Create the File
Writing a command for QtPy-Rant CLI Client is very simple. First,
make a python file in `rantlib/core_application/nogui/command`. **The**
**file must start with cmd_ to be dynamically imported**. Example: 
`cmd_helloworld.py`

## 2) Create the Class
Inside `cmd_helloworld.py`, you need to import the `Command` class from
`rantlib.core_application.nogui.command` and write a class that extends it

You'll probably want to implement the constructor and the `execute`
functions. The `execute` function in our class will just print
out "Hello World" no matter what arguments are passed to it.

```python
from rantlib.core_application.nogui.command import Command

class HelloWorldCommand(Command):

    def __init__(self):
        super().__init__()

    def execute(self, args):
        print("Hello world!")
```

## 3) Register the Command
Next, you need to register your command. The dynamic importer
calls a global function `register` with the `client` as an argument.
You need to use the client's 
`register_command(name, executor, alias=None, overwrite=False)`
method.

The `name` argument is the command the user will type in order
to execute your command. The `executor` is an instance of your class.
`alias` can be a string or list of strings, and if `overwrite` is
`True`, it will overwrite any other commands with the same name.

```python
def register(client):
    client.register_command("helloworld", HelloWorldCommand())
```

Now, if the user executes the command, they will see our message
print out:

```
>> helloworld
Hello world!
>> |
```

All together, that's:

```python
from rantlib.core_application.nogui.command import Command

class HelloWorldCommand(Command):

    def __init__(self):
        super().__init__()

    def execute(self, args):
        print("Hello world!")

def register(client):
    client.register_command("helloworld", HelloWorldCommand())
```
*Note that the register function is in the global scope and is not*
*a member function of the HelloWorldCommand class*

## Tips
It is a good idea to pass the client to the class in it's constructor
because the client has lots of useful information that the command
may need, including the `qtpy` application object, and config objects.

Implement the `usage` and `description` member variables, and the `help`
member function. Otherwise, the user will see default text when using
the `help` command.

*By default, the help function just prints out the command's usage*

The `usage` should follow a similar format to other usages. Try using
the `help` command to get an idea. A question mark denotes an optional
field. For example, the echo command can be called with or without
arguments:

```
Usage: echo <?arguments>
```

The helloworld command takes no arguments, so the usage would
be

```
Usage: helloworld
```

Which you would set in the constructor:

```python
class HelloWorldCommand(Command):

    def __init__(self):
        super().__init__()
        self.usage = "helloworld"
```

**Note**: the base Command class fills in the "Usage: " part. You should
not include this in your member variable. Instead, if you want to print
out the usage, use `Command.help(self)`

# Commands in Depth

Base class member variables:

* `description` - `<str>`: A short description of your command
* `parser` - `<ArgParser|None>`: Commands support `argparse.ArgParser`s
* `usage` - `<str>`: Usage guidance string

Base class methods:

* `help`: Executed when the help command is used on your command
* `execute`: Called when your command is called by the user

## description
The help command reads this field when listing all available
commands. The help command lists all available commands when
it is executed without any arguments.

## parser
By default, this field is `None`. In this case, a **simple** parse
of arguments is performed: you will recieve an array of strings
split up by spaces. Example:

```
>> helloworld this is an argument
['this', 'is', 'an', 'argument']
>> helloworld "this is an argument"
['"this', 'is', 'an', 'argument"']
>> |
```

However, if the `parser` field is not `None`, it will assume that
it is an instance of a `ArgumentParser` class. This allows for
more complex argument parsing. Any argument parser's `error` method
is also overridden by the client to avoid crashing if the user passes
invalid arguments to your command


## usage
Usage should be a simple, understandable string which demonstrates the
syntax of your command. Optional arguments should be denoted with a
question mark "?" (or equivalent in your language).

The base `help` function simply prints `"Usage: " + self.usage`

If you want to print the usage in a standard manner, use `Command.help(self)`

## help
The help method takes no arguments, but allows you to create a more
complex user help flow. If the help command is used with your command
as an argument...

```
>> help helloworld
```

...your executor's `help` function is called. If you want to write
more that just the usage, or even create a more interactive experience,
you must implement this method. Otherwise, the base class will
print out the usage string.

## execute
The most important part of your command is the `execute` method. This
is what is called with the user executes your command

```
>> helloworld
```

You will recieve a `CommandInput` object with two items:

* `args`: Object
* `raw_text`: str

The raw text is all of the text of the arguments (The command is removed):
```
>> helloworld this is an argument
'this is an argument'
```

`args` depends on whether you have set your `parser` member variable.
[Read more](#parser) about the args object's potential values