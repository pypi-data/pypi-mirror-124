import os
import yaml

from hi.resources.main import Deployment
from hi.utils.errors import ParamError
from hi.utils.search import deep_merge


class HelmDeployment(Deployment):
    def __init__(self, releases, repositories, bases):
        self.releases = releases
        self.repositories = repositories
        self.bases = bases

    @classmethod
    def read_from_yaml_file(cls, path, constructor_vars = {}):
        values = super().read_from_yaml_file(path, constructor_vars)
        for stages in list(values['releases'].values()):
            for desc in list(stages.values()):
                if 'values_files' in desc:
                    for f_path in desc['values_files']:
                        if not f.startswith('/'):
                            f_path = os.path.abspath(f"{ os.path.dirname(path) }/{ f_path }")

                        with open(f_path, 'r') as f:
                            desc['values'] = deep_merge(desc['values'], yaml.safe_load(f.read()))

        return HelmDeployment(
            values['releases'],
            values['repositories'],
            values.get('bases')
        )

class HelmRelease:
    def __init__(self, name, namespace, chart, chart_version, chart_repo, values):
        # namespace, chart, chart_version, chart_repo = None, values = {}):
        if not name:
            raise ParamError("No name provided for this helm release.")
        if not namespace:
            raise ParamError("No namespace provided for this helm release.")
        if not chart:
            raise ParamError("No chart provided for this helm release.")
        if not chart_version:
            raise ParamError("No chart version provided for this helm release.")

        self.name = name
        self.namespace = namespace
        self.chart = chart
        self.version = chart_version
        self.chart_repo = chart_repo
        self.values = values
        # self.service = service
        self.wait = True
