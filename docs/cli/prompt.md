# CLI mode prompt
*Probably the most fun feature of the whole client, if I'm honest*

The *prompt* is the text which is printed before you input a command
in the command-line interface, which indicates that the program is
ready to recieve commands. It can also display some useful data. The
prompt is rendered from a "formula": the `prompt` setting, found
in your configuration. You can modify this value with the set command
or in the configuration file directly (which would require an
application restart, obviously).

The syntax for prompts is very simple: anything within square
brackets is interpreted as an "instruction", and anything
outside square brackets is considered plain text and is printed
as-is. The default prompt is:

```
[green_fg][user] [reset]>> 
```

It is important to note that prompt "instructions" are also
referred to as prompt "gadgets".

There are a few things you may have noticed. For one, the prompt
isn't green by default. This is because colors are turned off
by default†1 due to the inability to guarantee color functionality
across all terminal emulators and platforms. Second, you will
notice that `[user]` is replaced with the current application
user. This will be "Guest" for users whom are not logged in, and
the username of a logged in user.  `[reset]` resets the formatting
for the console back to default (or as close as possible), and
then `>> ` is interpreted as text. Note the extra space after
the double chevron, which gives the user some padding (just 
for looks).

†1 You can enable colors with `set preference_colors_enabled True`.
It is recommended you enable colors. They look great.

Modifying the prompt is very easy. Let's take out all the
instructions.

```
set prompt >> 
```

Now you will just see something like this:

```
>> |
```

If you want to restore your prompt, it is a restorable setting.
Use `set --restore prompt`.

There are tons of instructions. A list of all of the built-in
instructions (which must be surrounded with square brackets
and are case-sensitive)

* the ASCII colors (see below)
* reset - reset terminal formatting
* user - the current user or "guest"
* time12 - 12 hour formatted time
* time, time24 - 24 hour formatted time
* hour
* minute
* second
* am - AM/PM for 12 hour time
* user_id - current user id or nothing for anon users
* app_version - QtPy-Rant version
* client_version - CLI mode client version
* command_count - the current count of commands run
* date - formatted date
* date_short - formatted date, using abbreviations
* day, day_name - the name of the current day
* day_name_short - the name of the current day, abbreviated
* day_of_week_number - 0 to 6
* day_number - day of the month, numerical
* year - four digit year
* year_short - two digit year (*obligatory Y2K warning*)
* month, month_name: the name of the current month
* month_name_short: the name of the current month, abbreviated
* month_number
* timezone

## Colors
By default, colors are ***disabled***, so you may not see
changes, and that's why. Only the 7 ASCII colors (red, green,
blue, yellow, magenta, cyan, white (and black)) are supported
with no plans to support any more. Both foreground and
background are supported. This is the formula for colors:

```
[(color name)_(fg or bg)]
```

For example, red foregorund:

```
[red_fg]
```

Another example, white background:

```
[white_bg]
```

***colors are not guaranteed to work on all platforms***
***or in all terminal emulators***

To reset the terminal's formatting to its default state,
use `[reset]`

## Command prompts

Any command may or may not be available to use in a prompt.
To check, you can use the help command.

```
>> help rant
...
Prompt gadget: False
...
```

This makes the number of prompt gadgets beyond the built-in
ones infinite. You can even create your own gadget! See the
[documentation](command) on writing your own command to do so.