import os
import yaml
import random
import string


def get_valid_file(paths = []):
    for p in paths:
        if os.path.exists(p):
            return p
    
    return None


def replace_in_file(path, pattern, replace):
    with open(path, "r") as f:
        content = f.read().replace(pattern, replace)
    
    with open(path, "w") as f:
        f.write(content)

def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    return result_str

def deep_merge(a, b, path=None):
    "merges b into a"

    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                deep_merge(a[key], b[key], path + [str(key)])
            elif isinstance(a[key], list) and isinstance(b[key], list):
                a[key].extend(b[key])
            elif a[key] != b[key]:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a
