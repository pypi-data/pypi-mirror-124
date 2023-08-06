import os
from hi.resources.cloudformation import CFDeployment
from hi.utils.search import deep_merge
import yaml

from hi.resources.main import Deployment, ReleaseDetails, Resource
from hi.utils.errors import ParamError

from hi.config import configuration


class InfraResource(Resource):
    def __init__(self, name, path, resource_type):
        super().__init__(name, path)
        self.resource_type = resource_type

class InfraK8sDeployment(Deployment):
    def __init__(self, name):
        self.image_name = self.get_service(name)
        self.name = self.image_name[3:] if self.image_name.startswith('hi.') else self.image_name
        self.path = configuration.infra.services[self.name]

    def get_helmfile_paths(self):
        return [
            f"{ self.path }/deployment/helm.yaml",
            f"{ self.path }/.gitlab/deployment/helm.yaml"
        ]

    @classmethod
    def get_service(cls, service):
        services_in_stage = list(configuration.infra.services.keys())

        if not service:
            current_path = os.getcwd()

            for p in current_path.split('/')[::-1]:
                if p in services_in_stage:
                    return
                    break

            if not service:
                raise ParamError(f"Service name not provided and unable to retrive from current path: { current_path }")

        if service not in configuration.infra.services:
            raise ParamError(f"Service '{ service }' is not currently supported")

        return service

class InfraFactory:
    def __init__(cls, resource, details):
        pass

class LoadBalancer(InfraFactory):
    @classmethod
    def get_deployment(cls, resource: InfraResource, details: ReleaseDetails):
        _, stack_template = CFDeployment.read_from_yaml_file(resource.path, { 'resource': resource })

        # final_resource_list = list(stack_template['Resources'].keys())
        # for key, val in stack_template['Resources'].items():
        #     if val['Type'] == "AWS::ElasticLoadBalancingV2::TargetGroup" and not val['Properties']['Targets']:
        #         final_resource_list.remove(key)
        #         final_resource_list.remove(f"Listener{ key[11:] }")

        # final_resources = {}
        # for name in final_resource_list:
        #     final_resources[name] = stack_template['Resources'][name]

        # stack_template['Resources'] = final_resources
        return CFDeployment(f"hi-{ details.stage }-loadbalancer-{ resource.name }", stack_template)
