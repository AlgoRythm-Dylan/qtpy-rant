from os.path import expanduser
from os.path import join
import os
import sys
import json
from rantlib.core_application.ui.window.window_state import WindowState

def get_data_dir_path():
    return join(expanduser("~"), ".qtpy-rant")

def get_dir(path=get_data_dir_path()):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

STD_PATH_AUTH = join(get_dir(), "auth.json")
STD_PATH_APP_CONFIG = join(get_data_dir_path(), "app-config.json")
STD_PATH_CLI_CONFIG = join(get_data_dir_path(), "cli-config.json")
STD_PATH_GUI_CONFIG = join(get_data_dir_path(), "gui-config.json")
STD_PATH_WINDOW_STATE = join(get_data_dir_path(), "window_state/")

def read_window_state(class_name):
    state_data = read_data_file(join(get_dir(STD_PATH_WINDOW_STATE), f"{class_name}.json"))
    window_state = WindowState()
    if state_data != None:
        window_state.data(state_data)
    return window_state

def write_window_state(class_name, window_state):
    return write_data_file(join(get_dir(STD_PATH_WINDOW_STATE) + f"/{class_name}.json"), window_state)

# Returns data file contents or `default` if file does not exist
# Expects JSON data
def read_data_file(path, default=None, print_error=False):
    data = default
    try:
        file = open(path, "r")
        data = json.loads(file.read())
        file.close()
    except Exception as e:
        if print_error:
            print(e, file=sys.stderr)
    return data

# json.dumps is really dumb and ONLY works with primitive types
def complex_encoder(obj):
    return obj.__dict__

def write_data_file(path, data):
    file = open(path, "w+")
    file.write(json.dumps(data, default=complex_encoder))
    file.close()
    