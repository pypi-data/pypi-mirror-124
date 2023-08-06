# import click
# from hi.resources.service import ServiceResource

# from hi.config import configuration
# from hi.engines.helm import get_history
# from hi.resources import HelmRelease


# @click.command("helm/history", help = "Deploy a service via helm")
# @click.option('--stage', '-e', type=click.Choice(configuration.stages.helm), default="default", help="Stage to deploy to")
# @click.option('--service', '-s', type=click.Choice(configuration.accepted_services), help="Service to deploy")
# def helm_deploy(service, stage):
#     s = ServiceResource(service)
#     helm = HelmRelease(s)

#     print(f":: History for {helm.name} in { stage }")
#     for h in get_history(helm, stage):
#         print(h)


# @click.command("helm/deploy", help = "Deploy a service via helm")
# @click.option('--stage', '-e', type=click.Choice(configuration.stages.helm), default="default", help="Stage to deploy to")
# @click.option('--service', '-s', type=click.Choice(configuration.accepted_services), help="Service to deploy")
# @click.option('--helmfile', '-f', help="Path to the helmfile.yaml")
# @click.option('--image-tag', '-i', help="The image tag to deploy")
# def helm_deploy(service, stage, helmfile):
#     helm = HelmRelease(service, stage, helmfile)

#     print(f":: Deploying {helm.name} to { stage } via helm")
#     deploy(helm, stage)

# @click.command("helm/rollback", help="Rollback a service")
# @click.option('--stage', '-e', help="Stage where to rollback", type=click.Choice(configuration.stages.helm), default="dev")
# @click.option('--service', '-s', help="Service to rollback", type=click.Choice(configuration.accepted_services), required=True)
# def helm_rollback(stage, service):
#     helm = HelmRelease(service, stage, None)
#     print(f":: Rolling back { helm.name } in { helm.stage } via helm")

#     rollback(helm)


# @click.command("helm/template", help="Print the values file for a service in a stage")
# @click.option('--stage', '-e', help="Stage where to rollback", type=click.Choice(configuration.stages.helm), default="dev")
# @click.option('--service', '-s', help="Service to rollback", type=click.Choice(configuration.accepted_services))
# @click.option('--output', '-o', help="Output path")
# def helm_template(stage, service, output):
#     helm = HelmRelease(service, stage)

#     print(f":: Helm values template for { helm.name } in { helm.stage }")
#     temp = yaml.dump(template(helm))
#     if output:
#         with open(output, "w") as f:
#             f.write(temp)
#     else:
#         print(temp)


# @click.command("helm/current", help="Get current deploy info for a service")
# @click.option('--stage', '-e', help="Stage to check", type=click.Choice(configuration.stages.helm), default="dev")
# @click.option('--service', '-s', help="Service to check", type=click.Choice(configuration.accepted_services))
# def helm_current(stage, service):
#     helm = HelmRelease(service, stage)
#     print(f":: Current { helm.name } in { helm.stage }:")

#     releaser, commit, dirty, deploy_date, branch = current(helm)

#     print(f"- Releaser: { releaser }")
#     print(f"- Commit: { commit }")
#     print(f"- Dirty: { dirty }")
#     print(f"- Deploy date: { deploy_date }")
#     print(f"- Branch: { branch }")


# @click.command("helm/remove", help="Remove a service from EKS")
# @click.option('--service', '-s', type=click.Choice(configuration.accepted_services), help="Service to uninstall", required=True)
# @click.option('--stage', '-e', type=click.Choice(configuration.stages.all), help="The stage of the service to uninstall")
# @click.option('--confirm', prompt="You're about to uninstall a service. Recovery from this will need manual input (y/N)", help='Confirm whether you want to delete', default="N")
# def helm_remove(stage, service, confirm):
#     if confirm.lower() in [ "y", "yes"]:
#         s = Service(stage, service)
#         remove(s)
#     else:
#         print("Aborting")
