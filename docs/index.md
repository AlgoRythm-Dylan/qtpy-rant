# QtPy-Rant

QtPy-Rant is essentially a 2-in-1 client for devRant: a
command-line client and a Qt-based graphical client.

The default client is graphical, but adding the `--nogui`
switch will enter the CLI client.

QtPy-Rant uses `pyqt5` and `requests` pip modules.

```
python3 qtpy-rant.py --nogui
```

Quick access to docs:
* [Learn how to edit your CLI prompt](cli/prompt)
* [Learn how to write a custom command](cli/command)