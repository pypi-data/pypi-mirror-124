import boto3
import botocore
import re
from hi.utils.errors import ParamError
from hi.utils.search import deep_merge, get_valid_file
import yaml

from hi.resources.cloudformation import CFDeployment, CFRelease
from hi.resources.main import ReleaseDetails, ReleaseMetadata, Resource
from hi.utils.yaml_cf_utils import SafeUnknownDumper

class DeployError(Exception):
    def __init__(self, msg):
        self.message = msg
    
    def __str__(self):
        return self.message


def check_stack_exists(cf: CFRelease):
    client = boto3.client('cloudformation')

    try:
        client.describe_stacks(
            StackName=cf.stack_name,
        )
        return True
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Message'] == f"Stack with id { cf.stack_name } does not exist":
            return False
        else:
            raise error

def create_stack(cf: CFRelease):
    client = boto3.client('cloudformation')
    client.create_stack(
        StackName=cf.stack_name,
        TemplateBody=cf.stack_template,
        # OnFailure="DELETE"
    )

def update_stack(cf: CFRelease):
    client = boto3.client('cloudformation')
    client.update_stack(
        StackName=cf.stack_name,
        TemplateBody=cf.stack_template
    )

def deploy(cf: CFRelease):
    client = boto3.client('ecs')

    try:
        task_definition = client.describe_task_definition(
            taskDefinition=cf.task_name
        )['taskDefinition']
    except botocore.exceptions.ClientError as error:
        if error.response['message'] == "Unable to describe task definition.":
            if not check_stack_exists(cf):
                create_stack(cf)
            else:
                raise Exception(f"Can't describe task { cf.task_name } nor create stack { cf.stack_name }")
        else:
            raise error

    task_definition['containerDefinitions'] = cf.containers
    del task_definition['taskDefinitionArn']
    del task_definition['revision']
    del task_definition['status']
    del task_definition['requiresAttributes']
    del task_definition['compatibilities']
    del task_definition['registeredAt']
    del task_definition['registeredBy']

    registration = client.register_task_definition(
        **task_definition
    )

    client.update_service(
        cluster = cf.cluster_name,
        service = cf.task_name,
        taskDefinition = registration['taskDefinition']['taskDefinitionArn']
    )


def rollback(cf: CFRelease):
    client = boto3.client('ecs')

    current_task_arn = client.describe_task_definition(
        taskDefinition=cf.task_name
    )['taskDefinition']['taskDefinitionArn']

    matches = re.match('(.+)(\d+)$', current_task_arn)
    client.update_service(
        cluster = cf.cluster_name,
        service = cf.task_name,
        taskDefinition = f"{ matches.group(1) }{ int(matches.group(2))-1 }"
    )


def remove(cf: CFRelease):
    client = boto3.client('ecs')

    client.delete_service(
        cluster = cf.cluster_name,
        service = cf.task_name
    )


def template(cf: CFRelease):
    return yaml.dump(cf.stack_template, Dumper=SafeUnknownDumper)


def get_current_release_details(cf: CFRelease, metadata_class):
    client = boto3.client('ecs')

    current_deployment = client.describe_services(
        cluster = cf.cluster_name,
        services = [cf.task_name]
    )['services'][0]['deployments'][0]

    metadata = __get_details_for_task(current_deployment['taskDefinition'], cf.container_name, metadata_class)
    metadata['deploy_date'] = current_deployment['createdAt']
    
    return ReleaseMetadata(metadata)


def get_history(cf: CFRelease, max: int = 50, with_metadata = None):
    client = boto3.client('ecs')
    current_arn = client.describe_task_definition(
        taskDefinition=cf.task_name
    )['taskDefinition']['taskDefinitionArn']
    current_arn_revision = int(current_arn.split(':')[-1])
    revision = current_arn_revision

    current_deployment = client.describe_services(
        cluster = cf.cluster_name,
        services = [cf.task_name]
    )['services'][0]['deployments'][0]

    history = []
    if with_metadata:
        while revision > 0 and revision > (current_arn_revision - max):
            metadata = __get_details_for_task(f"{ cf.task_name }:{ revision }", cf.container_name, with_metadata)
            metadata['deploy_date'] = None if revision != current_arn_revision else current_deployment['createdAt']
            history.append(ReleaseMetadata(metadata))
            revision = revision - 1

    return history[::-1]


def __get_details_for_task(task_name, container_name, metadata_class):
    client = boto3.client('ecs')

    current_task = client.describe_task_definition(
        taskDefinition=task_name
    )

    container = __get_container_for_task(current_task, container_name)
    metadata = metadata_class.metadata_from_cf_container(container)
    metadata['tag'] = container['image'].split(':')[-1]
    return metadata


def __get_container_for_task(task, container_name):
    for container in task['taskDefinition']['containerDefinitions']:
        if container['name'] == container_name:
            return container

    raise ParamError(f":: Container { container } not found in task.")


def get_cf_release_for_service(service: Resource, details: ReleaseDetails, metadata: ReleaseMetadata):
    cf_deployment_file = get_valid_file(service.get_cf_paths())

    deploy_desc = CFDeployment.read_from_yaml_file(cf_deployment_file, { 'service': service, 'release': details, 'metadata': metadata })

    cluster, container, task, stack = service.get_cf_details(details.stage)

    stack_template = deploy_desc.stack_template

    merged_stage = deep_merge(deploy_desc.stages.get('all') or {}, deploy_desc.stages[details.stage])

    for param, value in merged_stage['parameters'].items():
        stack_template['Parameters'][param]['Default'] = value

    stack_template['Resources']['TaskDefinition']['Properties']['ContainerDefinitions'] = [ container for container in list(merged_stage['containerDefinitions'].values()) ]

    return CFRelease(task, cluster, stack, container, stack_template)
