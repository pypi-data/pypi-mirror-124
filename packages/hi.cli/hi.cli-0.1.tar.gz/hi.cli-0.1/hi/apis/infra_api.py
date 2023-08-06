import click
from hi.engines.cloudformation import check_stack_exists, create_stack, update_stack
from hi.engines.infra import CLUSTER_RESOURCES, get_cluster_resource, get_stage_resource
from hi.engines.k8s import delete_pods, list_pods_in_namespace
from hi.resources.main import ReleaseDetails
import yaml

from hi.config import configuration
from hi.engines.helm import get_helm_main_release, get_helm_releases_for_service, rollback as helm_rollback, deploy as helm_deploy, remove as helm_remove, logs as helm_logs, template as helm_template
from hi.engines.charts import package as charts_package, push as charts_push
from hi.resources import InfraResource, Chart

# @click.command("infra/deploy", help="Deploy to an infrastructure component to a stage")
# @click.option('--stage', '-e', help="Stage to deploy the infrastructure component into", type=click.Choice(configuration.stages.helm), default="dev")
# @click.option('--resource-type', '-t', help="Type of the resource", required=False)
# @click.option('--name', '-n', help="Component to deploy", required=False)
# @click.option('--release', '-r', help="Which release", default="main")
# def infra_deploy(stage, name, resource_type, release):
#     inf = InfraResource(name)

#     rel_details = ReleaseDetails(
#         stage,
#         inf.name,
#         None,
#         release
#     )

#     if resource_type == "deployments":
#         releases = get_helm_releases_for_service(inf, rel_details)
#         for rel in releases:
#             helm_deploy(rel)
#     else:
#         resource = get_k8s_or_cf_resource_object(inf, rel_details)
#         resource.

#     print(f":: Deploying {inf.name} in { stage }")
#     helm_deploy(inf, stage, release=release)
#     print(f":: Deployed {inf.name} in { stage }")


# @click.command("infra/rollback", help="Rollback an infrastructure component in the given stage")
# @click.option('--stage', '-e', help="Stage of the service", type=click.Choice(configuration.stages.helm), default="dev")
# @click.option('--service', '-s', help="Service to rollback", type=click.Choice(configuration.infra.accepted_services))
# @click.option('--release', '-r', help="Which release", default="main")
# def infra_rollback(stage, service, release):
#     resource = HelmRelease(InfraResource(service, stage))
#     print(f":: Rolling back {resource.name} in { stage }")
#     helm_rollback(resource, stage, release=release)


# @click.command("infra/logs", help="Check logs of an infrastructure component")
# @click.option('--stage', '-e', help="Stage of the infrastructure component", type=click.Choice(configuration.stages.helm), default="dev")
# @click.option('--service', '-s', help="Infrastructure component to check the logs of", type=click.Choice(configuration.infra.accepted_services), required=True)
# def infra_logs(stage, service):
#     helm_logs(HelmRelease(InfraResource(service, stage)))


# @click.command("infra/remove", help="Remove a service")
# @click.option('--service', '-s', type=click.Choice(configuration.infra.accepted_services), help="Service to remove", required=True)
# @click.option('--stage', '-e', type=click.Choice(configuration.stages.helm), help="The stage of the service to remove")
# @click.option('--confirm', prompt="You're about to remove a service. Recovery from this will need manual input (y/N)", help='Confirm whether you want to delete', default="N")
# @click.option('--release', '-r', help="Which release", default="main")
# def infra_remove(stage, service, confirm, release):
#     if confirm.lower() in [ "y", "yes"]:
#         resource = HelmRelease(InfraResource(service, stage))
#         print(f":: Remove {resource.name} in { stage }")
#         helm_remove(resource, stage, release=release)
#     else:
#         print("Aborting")


@click.command("infra/template", help="Get helm values for the service on stage")
@click.option('--service', '-s', type=click.Choice(configuration.infra.accepted_services), help="Service to remove", required=True)
@click.option('--stage', '-e', help="Stage to deploy the infrastructure component into", type=click.Choice(configuration.stages.helm), default="dev")
@click.option('--output', '-o', help="Where to write to")
@click.option('--releases', '-r', help="Which release", default="main")
def infra_template(service, releases, output, stage):
    inf = InfraResource(service)

    rel_details = ReleaseDetails(
        stage,
        inf.name,
        releases=releases
    )

    release = get_helm_releases_for_service(inf, rel_details)[0]

    print(f":: Values for { inf.name } on { stage }")

    temp = yaml.dump(helm_template(release))
    if output:
        with open(output, "w") as f:
            f.write(temp)
    else:
        print(temp)

@click.command("infra/chart", help="Package and push a chart")
@click.option('--chart', '-c', type=click.Choice(configuration.infra.accepted_charts), help="Chart to release", required=True)
def infra_chart(chart):
    chart = Chart.from_chart_yaml(chart)
    charts_package(chart)
    print(f":: Packaged{ chart }")
    charts_push(chart)
    print(f":: Pushed { chart } to hi-charts")


@click.command("infra/killbuilds", help="Kill all builds")
@click.option('--project', '-p', help="Which project to kill", default="all")
def infra_killall(project):
    pods = list_pods_in_namespace('builds')
    delete_pods(pods)


# @click.command("infra/resource", help="Render the template of an infra resource")
# @click.option('--type', '-t', help="Type of resources to render", required=True)
# @click.option('--stage', '-e', help="Stage for the resource", type=click.Choice(configuration.stages.all), default="dev")
# @click.option('--name', '-n', help="The name of the resource", required=True)
# @click.option('--output', '-o', help="Output path")
# def infra_resource(name, type, stage, output):
#     resource = InfraResource(name, type)

#     # rel_details = ReleaseDetails(
#     #     stage,
#     # )

#     # if not output:
#     #     print(content)
#     # else:
#     #     with open(output, "w") as f:
#     #         f.write(content)


@click.command("infra/lb/create", help="Deploy a loadbalancer")
@click.option('--stage', '-e', help="Stage for the resource", default="dev")
@click.option('--name', '-n', help="The name of the resource", type=click.Choice(CLUSTER_RESOURCES['loadbalancers'].keys()), required=True)
def loadbalancer_create(name, stage):
    deployment = get_cluster_resource(name, 'loadbalancers', stage)
    if not check_stack_exists(deployment):
        create_stack(deployment)
    else:
        update_stack(deployment)


# @click.command("infra/sg/create", help="Deploy a loadbalancer")
# @click.option('--stage', '-e', help="Stage for the resource", default="dev")
# @click.option('--name', '-n', help="The name of the resource", type=click.Choice(CLUSTER_RESOURCES['securitygroups'].keys()), required=True)
# def sg_create(name, stage):
#     deployment = get_cluster_resource(name, 'loadbalancers', stage)
#     if not check_stack_exists(deployment):
#         create_stack(deployment)
#     else:
#         update_stack(deployment)


# @click.command("infra/lb/delete", help="Delete a loadbalancer")
# @click.option('--stage', '-e', help="Stage for the resource", default="dev")
# @click.option('--name', '-n', help="The name of the resource", type=click.Choice(CLUSTER_RESOURCES['loadbalancers'].keys()), required=True)
# def loadbalancer_create(name, stage):
#     deployment = get_cluster_resource(name, 'loadbalancers', stage)
#     if not check_stack_exists(deployment):
#         create_stack(deployment)
#     else:
#         update_stack(deployment)
