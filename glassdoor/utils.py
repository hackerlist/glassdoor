import re

def intify(s):
    """Coerce string to int"""
    return int(re.sub("[^0-9]", "", s))

def tryelse(func, default='', exception=Exception, log=False):
    """
    """
    try:
        return func()
    except exception as e:
        if log:
            print e
        return default
