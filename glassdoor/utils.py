import re

def intify(s):
    """Coerce string to int"""
    return int(re.sub("[^0-9]", "", s))

def tryelse(func, default='', exception=Exception):
    """
    """
    try:
        return func()
    except exception as e:
        return default
