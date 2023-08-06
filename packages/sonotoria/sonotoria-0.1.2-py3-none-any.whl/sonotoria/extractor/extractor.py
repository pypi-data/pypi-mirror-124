import re

from .cast import ensure_data_types
from .dict_extractor import prepare_dicts_for_loop, extract_dict
from .cond_extractor import prepare_cond_template
from .var_extractor import prepare_var_template

ESCAPE_CHARS = ['(', ')', '?', '.']


def escape_char(tpl):
    for char in ESCAPE_CHARS:
        tpl = tpl.replace(char, f'\\{char}')
    return tpl

def add_border(tpl):
    return f'^{tpl}$'


def extract(template, input_):
    var_regex = escape_char(template)
    var_regex = add_border(var_regex)
    var_regex = prepare_var_template(var_regex)
    var_regex = prepare_cond_template(var_regex)
    var_regex, dicts = prepare_dicts_for_loop(var_regex)
    data = ensure_data_types(re.search(var_regex, input_).groupdict())
    return ensure_dict_data(data, dicts)


def ensure_dict_data(data, dicts):
    for dict_ in dicts:
        data[dict_['dict_name']] = extract_dict(dict_['content'], data[dict_['dict_name']], dict_)
    return data
