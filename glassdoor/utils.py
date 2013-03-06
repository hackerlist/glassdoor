import re

def intify(s):
    """Coerce string to int"""
    return int(re.sub("[^0-9]", "", s))

def tryelse(func, default=None):
    try:
        return func()
    except Exception as e:
        return default
