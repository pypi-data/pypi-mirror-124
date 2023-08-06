import re

def prepare_var_template(template):
    return re.sub(r'{{ *(.*?) *}}', r'(?P<\1>.*)', template)
