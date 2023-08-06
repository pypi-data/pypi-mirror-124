
import glob
from os.path import abspath

class Infra:
    def __init__(self, platform, charts = [], builders = []):
        self.platform = abspath(platform)
        self.charts = {}
        self.accepted_charts = []
        self.services = {}
        self.accepted_services = []
        self.builders = {}
        self.accepted_builders = []

        self.__build_chart_list(charts)
        self.__build_builders_list(builders)
        self.__build_services_list()

    def __build_chart_list(self, paths):
        for path in paths:
            for chart_path in glob.glob(path):
                chart_name = chart_path.split('/')[-1]

                self.charts[chart_name] = abspath(chart_path)
                self.accepted_charts.append(chart_name)

    def __build_services_list(self):
        for component_path in glob.glob(f"{ self.platform }/hi-dev/deployments/*"):
            service_name = component_path.split('/')[-1]
            self.services[service_name] = component_path
            self.accepted_services.append(service_name)

    def __build_builders_list(self, paths):
        for path in paths:
            for builder_path in glob.glob(path):
                builder_name = builder_path.split('/')[-1]
                self.builders[builder_name] = builder_path
                self.accepted_builders.append(builder_name)

class AWS:
    def __init__(self, user = None, dev = None, prod = None):
        self.user = user
        self.dev = dev
        self.prod = prod

    def get_profiles(self):
        profiles = []
        if self.dev:
            for profile, _ in self.dev.items():
                if profile != "default_profile":
                    profiles.append(profile)

        if self.prod:
            for profile, _ in self.prod.items():
                if profile != "default_profile":
                    profiles.append(profile)

        return profiles



class Gitlab:
    def __init__(self, token):
        self.token = token
        self.address = "https://gitlab.dev.hi.health/api/v4"
        self.headers = {"PRIVATE-TOKEN": self.token}


class Stages:
    def __init__(self, helm = [], cf = []):
        if not helm:
            self.helm = [
                'dev',
                'staging',
                'previews'
            ]
        if not cf:
            self.cf = [
                'test',
                'prod'
            ]

        self.all = self.helm + self.cf
