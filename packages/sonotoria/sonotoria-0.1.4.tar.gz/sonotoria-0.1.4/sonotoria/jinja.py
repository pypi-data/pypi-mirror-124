import jinja2

def template_string(str_, data, filters=None, tests=None):
    env = jinja2.Environment()
    for name, filter_ in (filters or {}).items():
        env.filters[name] = filter_
    for name, test in (tests or {}).items():
        env.tests[name] = test
    try:
        return env.from_string(str_).render(**data)
    except TypeError: # Yaml Objects
        return env.from_string(str_).render(**data.__dict__)
