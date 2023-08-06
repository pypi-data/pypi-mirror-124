import re

from .cast import try_cast


# {% for <key_name>, <value_name> in <dict_name>.items() %}<content>{% endfor %}


BEFORE_LOOP_NAME_REGEX = r'{%\s*for\s+(?P<key_name>\w+)\s*,\s*(?P<value_name>\w+)\s+in\s+'
AFTER_LOOP_NAME_REGEX = r'(?:\\\.items\\\(\\\))?\s+%}\n?(?P<content>.*?)\n?{%\s*endfor\s*%}'
DICT_FOR_LOOP_REGEX = BEFORE_LOOP_NAME_REGEX + r'(?P<dict_name>\w+)' + AFTER_LOOP_NAME_REGEX

def prepare_dicts_for_loop(template):
    dict_for_loops_data = [e.groupdict() for e in re.finditer(DICT_FOR_LOOP_REGEX, template, re.DOTALL)]
    template = re.sub(BEFORE_LOOP_NAME_REGEX, '(?P<', template, 0, re.DOTALL)
    template = re.sub(AFTER_LOOP_NAME_REGEX, r'>(\1\n?)*)', template, 0, re.DOTALL)
    return template, dict_for_loops_data

def extract_dict(template, input_, dict_):
    dict_values = {
        item[dict_['key_name']]: try_cast(item[dict_['value_name']])
        for item in re.finditer(template, input_)
    }
    return dict_values
