import os
from hi.utils.search import deep_merge
import yaml

from hi.resources.main import Deployment
from hi.utils.errors import ParamError
from hi.utils.yaml_cf_utils import CFYamlLoader, SafeUnknownConstructor, SafeUnknownDumper, all_fields_to_str, cf_lower_all_keys


class CFDeployment(Deployment):
    def __init__(self, stack_name, stack_template: dict):
        self.stack_name = stack_name
        self.stack_template = yaml.dump(stack_template, Dumper=SafeUnknownDumper)

    @classmethod
    def read_from_yaml_file(cls, path, constructor_vars = {}):
        values = super().read_from_yaml_file(path, constructor_vars)

        if 'stack' not in values:
            raise ParamError('Need a cloudformation stack to execute.')

        loader = CFYamlLoader
        loader.add_constructor(None, SafeUnknownConstructor.construct_undefined)
        with open(f"{ os.path.dirname(path) }/{ values['stack'] }", 'r') as f:
            stack_template = yaml.load(f.read(), Loader=loader)

        for param, value in values['Parameters'].items():
            stack_template['Parameters'][param]['Default'] = value

        if 'Resources' in values:
            stack_template['Resources'] = deep_merge(stack_template['Resources'], values['Resources'])

        return values, stack_template

class CFRelease:
    pass
