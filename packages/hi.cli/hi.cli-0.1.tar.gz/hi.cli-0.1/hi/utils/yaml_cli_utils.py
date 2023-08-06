import re
import os
import yaml

from yaml.loader import SafeLoader

class CLIYamlConstructor(yaml.constructor.SafeConstructor):
    def __init__(self, vars):
        self.vars = vars

    def sub(self, loader, node):
        matches = re.findall('{{ (var|env) (\w+)(?:\.(\w+))? }}', node.value)
        value = node.value
        for m in matches:
            val = None
            if not m:
                raise Exception("Couldn't retrieve sub")

            if m[0] == 'var':
                val = getattr(self.vars[m[1]], m[2])
                value = re.sub(f"{{{{ var { m[1] }\.{ m[2] } }}}}", val, value)
            elif m[0] == "env":
                val = os.environ.get(m[1]) or ""
                value = re.sub(f"{{{{ env { m[1] } }}}}", val, value)

        return value

    def var(self, loader, node):
        match = re.search('([\w\_\-\d]+)\.([\w\_\-\d]+)', node.value)
        return getattr(self.vars[match.group(1)], match.group(2))

    def env(self, loader, node):
        return os.environ.get(node.value)

    def ref(self, loader, node):
        return f"{ node.tag } { node.value }"

class CLIYamlLoader(SafeLoader):
    pass


def read_cli_yaml(path, constructor_vars = {}):
    constructor = CLIYamlConstructor(constructor_vars)
    loader = CLIYamlLoader
    loader.add_constructor(u'!Env', constructor.env)
    loader.add_constructor(u'!Var', constructor.var)
    loader.add_constructor(u'!Sub', constructor.sub)
    loader.add_constructor(u'!Ref', constructor.ref)

    with open(os.path.abspath(path), "r") as f:
        content = yaml.load(f.read(), Loader=loader)

    return content


def multiread_cli_yaml(path, constructor_vars = {}):
    constructor = CLIYamlConstructor(constructor_vars)
    loader = CLIYamlLoader
    loader.add_constructor(u'!Env', constructor.env)
    loader.add_constructor(u'!Var', constructor.var)
    loader.add_constructor(u'!Sub', constructor.sub)

    with open(os.path.abspath(path), "r") as f:
        content = yaml.load_all(f.read(), Loader=loader)

    return content
