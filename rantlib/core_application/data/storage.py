from os.path import expanduser
from os.path import join
import os
import sys
import json

def create_data_dir():
    os.mkdir(get_data_dir_path())

def get_data_dir_path():
    return join(expanduser("~"), ".qtpy-rant")

STD_PATH_AUTH = join(get_data_dir_path(), "auth.json")
STD_PATH_CLI_CONFIG = join(get_data_dir_path(), "cli-config.json")

# Returns data file contents or `default` if file does not exist
# Expects JSON data
def read_data_file(path, default=None):
    data = default
    try:
        file = open(path, "r")
        data = json.loads(file.read())
        file.close()
    except Exception as e:
        print(e, file=sys.stderr)
    return default

def write_data_file(path, data):
    file = open(path, "w+")
    file.write(json.dumps(data))
    file.close()
    