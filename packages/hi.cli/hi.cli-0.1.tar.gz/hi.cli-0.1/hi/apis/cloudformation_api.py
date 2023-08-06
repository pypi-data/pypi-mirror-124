# import click

# from hi.config import configuration
# from hi.engines.cloudformation import deploy, remove, rollback, template
# from hi.resources import CFRelease


# @click.command("cloudformation/deploy", help="Deploy a service to ECS")
# @click.option('--stage', '-e', type=click.Choice(configuration.stages.all), help="The stage to deploy to", default="test")
# @click.option('--service', '-s', type=click.Choice(configuration.accepted_services), help="The service to deploy")

# @click.option('--task', '-t', help="The image tag to deploy")
# @click.option('--cluster', '-c', help="The image tag to deploy")
# @click.option('--stack', '-s', help="Stack name")
# @click.option('--template', '-f', help="Template path")
# @click.option('--image-tag', '-i', help="Commit of the image")
# def cloudformation_deploy(stage, service, cluster, stack, template):
#     if 
#     CFRelease(task, )
#     cf = CFRelease(service, stage)
#     print(f":: Deploying { cf.name } to { stage } via helm")

#     deploy(cf, stage)


# @click.command("cloudformation/rollback", help="Rollback a service in ECS")
# @click.option('--service', '-s', type=click.Choice(configuration.accepted_services), help="Path to the file containing the cf template", required=True)
# @click.option('--stage', '-e', type=click.Choice(configuration.stages.all), help="The stage of the service to rollback", required=True)
# def cloudformation_rollback(stage, service):
#     cf = CFRelease(service, stage)
#     print(f":: Rolling back { cf.name } in { stage } via helm")

#     rollback(cf)

# @click.command("cloudformation/remove", help="Remove a service from ECS")
# @click.option('--service', '-s', type=click.Choice(configuration.accepted_services), help="Service to remove", required=True)
# @click.option('--stage', '-e', type=click.Choice(configuration.stages.all), help="The stage of the service to remove", required=True)
# @click.option('--confirm', prompt="You're about to remove a service. Recovery from this will need manual input (y/N)", help='Confirm whether you want to delete', default="N")
# def cloudformation_remove(stage, service, confirm):
#     if confirm.lower() in [ "y", "yes"]:
#         cf = CFRelease(service, stage)
#         remove(cf, stage)
#     else:
#         print("Aborting")

# # @click.command("cloudformation/stack/remove")
# # @click.option('--name', '-n', help="The name of the stack to remove")
# # @click.option('--confirm', prompt="You're about to REMOVE A STACK. This is UNRECOVERABLE (y/N)", help='Confirm whether you want to delete', default="N")
# # def cloudformation_remove(stage, service, confirm):
# #     if confirm.lower() in [ "y", "yes"]:
# #         service = get_service(service)
# #         client = get_aws_client('ecs')
        
# #         client.delete_service(
# #             cluster = f"hi-{ SHORT_STAGES[stage] }-ecs-cluster-services",
# #             service = f"hi-{ SHORT_STAGES[stage] }-ecs-service-{ service }"
# #         )
# #     else:
# #         print("Aborting")


# @click.command("cloudformation/template", help="Retrieve the cloudformation template for a service")
# @click.option('--template-path', '-t', help="Path to the file containing the cf template")
# @click.option('--params-path', '-p', help="Path to the file containing the parameters")
# @click.option('--stage', '-e', type=click.Choice(configuration.stages.cf), help="The stage to merge", default="test")
# @click.option('--service', '-s', type=click.Choice(configuration.accepted_services), help="The stage to merge")
# @click.option('--output', '-o', help="Output path")
# def cloudformation_template(service, template_path, params_path, stage, output):
#     cf = CFRelease(service, stage)
#     print(f":: Cloudformation template for { cf.name } in { stage }")

#     temp = template(template_path or cf.cf_template, params_path, stage)
#     if output:
#         with open(output, "w") as f:
#             f.write(temp)
#     else:
#         print(temp)
