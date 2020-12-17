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
# Note OCT 31 2020: I wish I could add airquotes to the "complex" part
# of this function
def complex_encoder(obj):
    return obj.__dict__

def write_data_file(path, data):
    file = open(path, "w+")
    file.write(json.dumps(data, default=complex_encoder))
    file.close()
    
def append_with_max(arr, data, max_len):
    while len(arr) + 1 > max_len:
        arr.pop()
    arr.append(data)
    return data

class DataClass:

    def __init__(self):
        self.accept_all_mode = False
        self.fill_missing_fields = True
        self.import_fields = {}
        self.ignore_fields = []
        self.translate_fields = {}

    def import_data_item(self, key, value):
        has_type_requirement = key in self.import_fields.keys()
        if not has_type_requirement and not self.accept_all_mode:
            return # Don't add this item
        type_requirement = self.import_fields.get(key, None)
        if isinstance(type_requirement, DataClass):
            type_requirement.import_data(value)
            self.__dict__[key] = value
        else:
            if type_requirement == object or type_requirement == None or type(value) == type_requirement:
                self.__dict__[key] = value
            else:
                try:
                    # Try to convert
                    self.__dict__[key] = type_requirement(value)
                except:
                    if self.fill_missing_fields:
                        self.__dict__[key] = None

    def import_data(self, data):
        translate_keys = self.translate_fields.keys()
        if self.accept_all_mode:
            for key, value in data.items():
                if not key in self.ignore_fields:
                    if key in translate_keys:
                        key = self.translate_fields[key]
                    self.import_data_item(key, value)
        else:
            import_keys = self.import_fields.keys()
            for key, value in data.items():
                if key in import_keys:
                    if key in translate_keys:
                        key = self.translate_fields[key]
                    self.import_data_item(key, value)
        self.init_fields()
        self.after_data_import(data)

    def init_fields(self):
        self_keys = self.__dict__.keys()
        import_field_keys = self.import_fields.keys()
        for key in import_field_keys:
            if not key in self_keys:
                self.__dict__[key] = None

    def after_data_import(self, data): # to be overridden by subclasses
        pass