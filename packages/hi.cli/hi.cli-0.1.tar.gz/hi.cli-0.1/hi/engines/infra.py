
import os
import re
from pathlib import Path
from hi.resources.helm import HelmDeployment
from hi.utils.search import deep_merge
import yaml

from hi.config import configuration
from hi.resources.infraservice import InfraResource, LoadBalancer
from hi.resources.main import ReleaseDetails

# base_path = os.path.dirname(os.path.realpath(os.path.abspath(__file__ + "/..")))

STAGES_DIR = f"{ configuration.infra.platform }/stages"
CLUSTERS_DIR = f"{ configuration.infra.platform }/clusters"


STAGES_RESOURCES = {}
CLUSTER_RESOURCES = {}
def discover_infra_resources():
    # Walk the tree.
    for stage in os.listdir(STAGES_DIR):
        for resource_type in os.listdir(f"{ STAGES_DIR }/{ stage }"):
            STAGES_RESOURCES[resource_type] = {}
            to_add = {}
            ignored_roots = []
            for root, _, files in os.walk(f"{ STAGES_DIR }/{ stage }/{ resource_type }"):
                for f in files:
                    if f == ".hi-ignore":
                        ignored_roots.append(root)
                        break

                    to_add[Path(f).stem] = { stage: os.path.join(root, f) }

            if root not in ignored_roots:
                STAGES_RESOURCES[resource_type] = deep_merge(STAGES_RESOURCES[resource_type], to_add)

    for cluster in os.listdir(CLUSTERS_DIR):
        for resource_type in os.listdir(f"{ CLUSTERS_DIR }/{ cluster }"):
            CLUSTER_RESOURCES[resource_type] = {}
            for root, _, files in os.walk(f"{ CLUSTERS_DIR }/{ cluster }/{ resource_type }"):
                to_add = {}
                ignore = False
                for f in files:
                    if f == ".hi-ignore":
                        ignore = True
                        break

                    to_add[Path(f).stem] = { stage: os.path.join(root, f) }

                if not ignore:
                    CLUSTER_RESOURCES[resource_type] = deep_merge(CLUSTER_RESOURCES[resource_type], to_add)

discover_infra_resources()

INFRA_RESOURCE_TYPES = {
    'deployments': HelmDeployment,
    'loadbalancers': LoadBalancer,
    # 'dynamodb': InfraK8sResource,
    # 'ecs': InfraCFRelease,
    # 'rds': InfraK8sResource,
    # 's3': InfraK8sResource,
    # 'sg': InfraK8sResource,
    # 'iam': InfraK8sDeployment,
    # 'route53': InfraK8sResource
}

# print(CLUSTER_RESOURCES)


def get_cluster_resource(name, resource_type, stage):
    resource = InfraResource(
        name = name,
        path = CLUSTER_RESOURCES[resource_type][name][stage],
        resource_type = resource_type
    )

    details = ReleaseDetails(
        stage,
    )

    return INFRA_RESOURCE_TYPES[resource.resource_type].get_deployment(resource, details)


def get_stage_resource(name, resource_type, stage):
    resource = InfraResource(
        name = name,
        path = STAGES_RESOURCES[resource_type][name][stage],
        resource_type = resource_type
    )

    details = ReleaseDetails(
        stage,
    )

    return INFRA_RESOURCE_TYPES[resource.resource_type].get_deployment(resource, details)
    


    # if resource.resource_type in INFRA_K8S_RESOURCES:
    #     pass
    # elif resource.resource_type in INFRA_CF_RESOURCES:
    #     path = f"{ configuration.infra.platform }/hi-{ details.stage }/infra/{ resource.resource_type }/{ resource.name }.yml"
    #     resource = INFRA_CF_RESOURCES[resource.type].read_from_yaml_file(path, { "resource": resource })

    #     print(yaml.dump(resource.stack_template, Dumper=SafeUnknownDumper))
    
    
    
    
    # templates = multiread_cli_yaml(INFRA_K8S_RESOURCE_TEMPLATES[resource.resource_type], { f"{ resource.resource_type }": resource, 'release': details })

    # content = ""
    # for t in templates:
    #     content += "---\n"
    #     content += yaml.dump(t)

    # return content


# def render_infra_cf_resource_template(resource: InfraCFResource, details: ReleaseDetails):
#     templates = read_cli_yaml(INFRA_RESOURCE_TEMPLATES[resource.resource_type], { f"{ resource.resource_type }": resource, 'release': details })

#     content = ""
#     for t in templates:
#         content += "---\n"
#         content += yaml.dump(t)

#     return content
