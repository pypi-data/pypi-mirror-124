import os
from re import S
import yaml
from hi.utils.search import deep_merge
from hi.utils.yaml_cli_utils import CLIYamlConstructor, CLIYamlLoader, read_cli_yaml


class Resource:
    def __init__(self, name, path):
        self.name = name
        self.path = path


class ReleaseMetadata:
    def __init__(self, fields):
        for k, v in fields.items():
            setattr(self, k, v)

    @classmethod
    def metadata_from_helm_values(values: dict):
        pass


class ReleaseDetails:
    def __init__(self, stage: str, image_name: str = "", image_tag: str = "", releases: str = 'all'):
        self.stage = stage
        self.image_name = image_name
        self.commit = image_tag
        self.releases = releases


class Deployment:
    @classmethod
    def read_from_yaml_file(cls, path, constructor_vars = {}):
        """
            Returns the file in path merged with all its base files
        """
        values = read_cli_yaml(path, constructor_vars)

        current_dir = os.path.dirname(path)
        if 'bases' in values:
            for base_path in values.get('bases'):
                with open(base_path if base_path.startswith('/') else f"{ current_dir }/{ base_path }", "r") as f:
                    constructor = CLIYamlConstructor(constructor_vars)
                    loader = CLIYamlLoader
                    loader.add_constructor(u'!Env', constructor.env)
                    loader.add_constructor(u'!Var', constructor.var)
                    loader.add_constructor(u'!Sub', constructor.sub)
                    loader.add_constructor(u'!Ref', constructor.ref)
                    values_to_merge = yaml.load(f.read(), Loader=loader)

                values = deep_merge(values, values_to_merge)

        return values
