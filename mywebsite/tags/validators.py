import re

def title(value):
    if value.startswith('#'):
        true_value = re.match(r'\#(\w+)', value)
        if true_value:
            value = true_value.group(1)
    value = value.lower()
    return value
