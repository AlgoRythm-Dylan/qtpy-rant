# QtPy-Rant
*The hackable, plugin-able, Qt-based, Python-powered devRant client*

Get the ultimate devRant experience by taking full advantage of your desktop's
power. Written in Python (hey, at least it's not fucking JavaScript) and using
Qt for GUI, this client is easy to develop and/or hack while still
maintaining the power of a full desktop programming language (one that
wasn't originally designed for the web!)

## Run it
Interested in previewing? Right now, the application is in pre-alpha. Don't
let that stop you, though. Install just three items and you're ready to go

```bash
git clone https://github.com/AlgoRythm-Dylan/qtpy-rant
# Install python3 and pip3 with your package manager
pip3 install requests
pip3 install PyQt5
# Once you're all installed, cd into the folder and run
cd qtpy-rant
# If you want the graphical version, run this:
python3 qtpy-rant.py
# Otherwise, add the --nogui switch for command-line mode
python3 qtpy-rant.py --nogui
```

Features:
- GUI and CLI clients
- Custom theme system
- Multiple logins
- Language support
- Installable command system
- Highly configurable
- Cross-platform terminal coloring (ASCII)

Planned:
- Fully-featured GUI and CLI clients
- Optional markdown renderer
- Fully-featured mod loader and modding system
- Notification preview and grouping
- Decent documentation
- Attention dispenser for Arch Linux users

Maybe:
- Avatar editor, if possible
- Bandwidth saving mode†1
- Rant archiver
- Outstanding documentation
- Important notifications†2

Probably not:
- Personal stats

†1 Do not load avatars, show "download image" button rather than
automatically downloading images, etc.

†2 Designate notifications from certain users or rants to show up in a 
different color, have a distinct count, and possibly make a sound