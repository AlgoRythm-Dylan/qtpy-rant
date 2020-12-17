from rantlib.app.storage import read_data_file
from pathlib import Path

def load_language(lang_code):
    # Load EN-US and given language and merge them
    lang_dir = Path(__file__).parent.parent.parent.joinpath("res").joinpath("lang")
    base_lang = {}
    lang = read_data_file(lang_dir.joinpath(f"{lang_code}.json"), default={})
    if lang_code != "EN-US":
        base_lang = read_data_file(lang_dir.joinpath("EN-US.json"))
    else:
        # Shortcut since we already loaded EN-US
        return lang
    for key, value in lang.items():
        base_lang[key] = value
    return base_lang

def simple_replace(template, replacements):
    for replacement, value in replacements.items():
        template = template.replace("{" + str(replacement) + "}", str(value))
    return template