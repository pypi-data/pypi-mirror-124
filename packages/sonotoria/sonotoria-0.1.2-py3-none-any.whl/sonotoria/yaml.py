import yaml

from .jinja import template_string

def load(path, filters=None, tests=None, types=None):
    for tag, type_ in (types or {}).items():
        add_data_type(tag, type_)

    context = {}
    with open(path, encoding='utf-8') as file:
        lines = file.readlines()

    content = []
    for line in lines:
        if '{{' not in line:
            content.append(line)
        else:
            context = yaml.safe_load('\n'.join(content))
            content.append(
                template_string(
                    line,
                    context,
                    filters = filters or {},
                    tests = tests or {}
                )
            )

    return yaml.safe_load('\n'.join(content))

def represent_ordered(dumper, data):
    return yaml.nodes.MappingNode(
        data.yaml_tag,
        [
            (
                dumper.represent_data(key),
                dumper.represent_data(getattr(data, key))
            )
            for key in data.attr_order
        ]
    )

def ordered(class_):
    yaml.add_representer(class_, represent_ordered)
    return class_

def constructed(class_):
    yaml.SafeLoader.add_constructor(class_.yaml_tag, class_.construct)

def add_data_type(tag, class_):
    class_.yaml_tag = f'!{tag}'
    try:
        constructed(class_)
    except AttributeError:
        class_.yaml_loader = yaml.SafeLoader
        new_class = type(f'Yaml{class_.__name__}', (yaml.YAMLObject,), {k: v for k, v in class_.__dict__.items() if not k.startswith('__')})
        if hasattr(new_class, 'attr_order'):
            ordered(new_class)
