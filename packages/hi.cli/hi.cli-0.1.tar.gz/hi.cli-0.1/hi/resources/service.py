import os

from hi.config import configuration
from hi.resources.cloudformation import CFDeployment, CFRelease
from hi.resources.main import ReleaseMetadata, Resource
from hi.utils.errors import ParamError
from hi.utils.yaml_cf_utils import all_fields_to_str, cf_lower_all_keys

class ServiceReleaseMetadata(ReleaseMetadata):
    def __init__(self, releaser: str = "", branch: str = "", dirty: bool = True):
        self.branch = branch
        self.dirty = dirty
        self.releaser = releaser

    @classmethod
    def metadata_from_helm_values(cls, values):
        if not 'env' in values:
            print(":: Environment variables could not be found for this release.")
            return {}

        return {
            'releaser': values['env'].get('DEPLOYED_BY'),
            'branch': values['env'].get('GIT_BRANCH'),
            'dirty': values['env'].get('GIT_IS_DIRTY')
        }

    @classmethod
    def metadata_from_cf_container(cls, container):
        if not 'environment' in container:
            print(":: Environment variables could not be found for this release.")
            return {}

        metadata = {
            'releaser': None,
            'branch': None,
            'dirty': None
        }

        for env in container['environment']:
            if env['name'] == 'DEPLOYED_BY':
                metadata['releaser'] = env['value']

            if env['name'] == 'GIT_BRANCH':
                metadata['branch'] = env['value']

            if env['name'] == 'GIT_IS_DIRTY':
                metadata['dirty'] = env['value']

        return metadata


class ServiceResource(Resource):
    def __init__(self, name):
        name = ServiceResource.get_service(name)
        super().__init__(
            name,
            configuration.services[name]
        )

        self.short_name = self.name.replace('hi.', '') if self.name.startswith('hi.') else self.name
        # self.repo = GitRepo(self.path)

    def get_dockerfile_paths(self):
        return [
            f"{ self.path }/.gitlab/docker/Dockerfile",
            f"{ self.path }/../.gitlab/docker/Dockerfile"
        ]

    def get_helmfile_paths(self):
        return [
            f"{ self.path }/deployment/helm.yaml",
            f"{ self.path }/.gitlab/deployment/helm.yaml"
        ]

    def get_cf_paths(self):
        return [
            f"{ self.path }/.gitlab/deployment/cloudformation.yml",
            f"{ self.path }/.gitlab/deployment/cloudformation.yaml",
            f"{ self.path }/../.gitlab/deployment/cloudformation.yml",
            f"{ self.path }/../.gitlab/deployment/cloudformation.yaml"
        ]

    @classmethod
    def get_service(cls, service):
        if not service:
            path = os.getcwd()

            for p in path.split('/')[::-1]:
                if p in configuration.services:
                    return p

            raise ParamError(f"Service name not provided and unable to retrive from current path: { path }")

        if not service.startswith('hi.'):
            service = f"hi.{ service }"

        if service not in configuration.services:
            raise ParamError(f"Service '{ service }' is not currently supported")

        return service

    def get_cf_details(self, stage):
        prefix = f"hi-{ stage }-ecs"
        cluster = f"{ prefix }-cluster-services"
        container = f"{ prefix }-container-{ self.short_name }"
        task = f"{ prefix }-service-{ self.short_name }"
        stack = f"{ task }-cf"

        return cluster, container, task, stack


class ServiceCFDeployment(CFDeployment):
    def __init__(self, stack_template, stages):
        super().__init__(stack_template)
        self.stages = stages

    @classmethod
    def read_from_yaml_file(cls, path, constructor_vars = {}):
        values, stack_template = super().read_from_yaml_file(path, constructor_vars)

        return ServiceCFDeployment(stack_template, values.get('stages'))


class ServiceCFRelease(CFRelease):
    def __init__(self, task_name, cluster_name, stack_name, container_name, stack_template):
        self.task_name = task_name
        self.cluster_name = cluster_name
        self.stack_name = stack_name
        self.container_name = container_name
        self.stack_template = stack_template

        self.containers = []
        for c in stack_template['Resources']['TaskDefinition']['Properties']['ContainerDefinitions']:
            c['Environment'] = all_fields_to_str(c['Environment'])
            if c['Name'] == self.container_name:
                c['HealthCheck']['Command'][0] = str(c['HealthCheck']['Command'][0])

            self.containers.append(cf_lower_all_keys(c))
