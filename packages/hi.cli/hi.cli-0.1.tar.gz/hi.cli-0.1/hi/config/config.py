import toml
import glob

from os import environ, listdir, getcwd
from os.path import isdir, join, abspath
from hi.engines import *

from hi.config.controllers import *

class NPM:
    def __init__(self, token):
        self.token = token


class Configuration:
    def __init__(self):
        self.stages = None
        self.aws = None
        self.google = None
        self.npm = None
        self.infra = None
        self.services = {}
        self.accepted_services = []
        self.repositories = []
        self.gitlab = []
        self.ecr_repository = "272371606098.dkr.ecr.eu-central-1.amazonaws.com"
        self.debug = False

    def load_file(self, path):
        try:
            override_config = toml.load(path)
        except:
            print("Configuration file not found.")
            override_config = {}

        if override_config.get('general'):
            if 'repositories' in override_config.get('general'):
                # self.repositories = Repositories(**override_config.get('repositories'))
                self.repositories = override_config.get('general').get('repositories')
        else:
            self.repositories = [f"{ getcwd() }/../hi.*"]

        self.aws = AWS(**override_config.get('aws')) if 'aws' in override_config else AWS()
        self.stages = Stages(**override_config.get('stages')) if 'stages' in override_config else Stages()

        if 'gitlab' in override_config:
            self.gitlab = Gitlab(**override_config.get('gitlab'))

        if 'infra' in override_config:
            self.infra = Infra(**override_config.get('infra'))

        if 'npm' in override_config:
            self.npm = NPM(**override_config.get('npm'))

        self.__build_service_list()


    def __build_service_list(self):
        services = {}
        accepted_services = []

        for repo in self.repositories:
            for path in glob.glob(repo):
                service_name = path.split('/')[-1]
                services[service_name] = abspath(path)
                accepted_services.append(service_name)
                if service_name.startswith("hi."):
                    accepted_services.append(service_name[3:])

        self.services = services
        self.accepted_services = accepted_services

    def get_short_stage(self, stage):
        return self.stages.get_short_stage(stage)

configuration = Configuration()

def init(path = f"{ environ['HOME'] }/.hi/config"):
    # print("Initializing config")
    global configuration
    configuration.load_file(path)
