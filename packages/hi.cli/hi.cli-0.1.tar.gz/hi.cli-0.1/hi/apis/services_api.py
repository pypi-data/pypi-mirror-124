import shutil
import click
import os

from hi.config import configuration
from hi.engines.cloudformation import get_cf_release_for_service, rollback as cf_rollback, deploy as cf_deploy, remove as cf_remove, get_current_release_details as cf_get_current_release_details, get_history as cf_get_history
from hi.engines.docker import build_remote, build_local
from hi.engines.k8s import get_pod_list_by_label, logs_for_pod
from hi.engines.gitlab import trigger_pipeline
from hi.engines.npm import build as npm_build
from hi.engines.helm import get_current_release_details, get_helm_main_release, rollback as helm_rollback, deploy as helm_deploy, remove as helm_remove, get_history as helm_get_history
from hi.resources import GitRepo, Image
from hi.resources.main import ReleaseDetails
from hi.resources.service import ServiceReleaseMetadata, ServiceResource
from hi.utils.search import get_valid_file, replace_in_file
from hi.utils.yaml_cf_utils import SafeUnknownDumper
import yaml
from yaml.dumper import Dumper


@click.command("services/deploy", help="Deploy to a service to a stage")
@click.option('--stage', '-e', help="Stage to deploy the service into", type=click.Choice(configuration.stages.all), default="dev")
@click.option('--service', '-s', help="Service to deploy", type=click.Choice(configuration.accepted_services), required=False)
@click.option('--image-tag', '-i', help="Image tag to use, defaults to the commit")
@click.option('--releaser', '-o', help="Releaser of this image")
@click.option('--branch', '-b', help="Branch of this image")
@click.option('--dirty/--not-dirty', help="Whether the image is dirty", default=True)
def services_deploy(stage, service, image_tag, branch, releaser, dirty):
    s = ServiceResource(service)

    repo = GitRepo(s.path)
    rel_details = ReleaseDetails(
        stage,
        s.name,
        image_tag or repo.get_commit()
    )

    metadata = ServiceReleaseMetadata(
        releaser or repo.get_releaser(),
        branch or repo.get_branch(),
        dirty=dirty
    )

    print(f":: Deploying {s.name} in { stage }...")
    if stage in configuration.stages.helm:
        helm_deploy(get_helm_main_release(s, rel_details, metadata))
    else:
        cf_deploy(get_cf_release_for_service(s, rel_details, metadata))

    print(f":: Deployed {s.name} in { stage }")

@click.command("services/release", help="Build and deploy a service")
@click.option('--stage', '-e', help="Stage of the service", type=click.Choice(configuration.stages.all), default="dev")
@click.option('--service', '-s', help="Service to deploy", type=click.Choice(configuration.accepted_services), required=False)
def services_release(stage, service):
    s = ServiceResource(service)
    repo = GitRepo(s.path)

    rel_details = ReleaseDetails(
        stage,
        s.name,
        repo.get_commit()
    )
    metadata = ServiceReleaseMetadata(
        repo.get_releaser(),
        repo.get_branch(),
        dirty=True
    )

    print(f":: Building { s.name } in { stage }")
    npm_build(s.path)

    print(f":: Building docker image for { s.name } in { stage }")
    build_local(
        Image(
            s.name,
            s.path,
            get_valid_file(s.get_dockerfile_paths()),
            tags=[rel_details.commit, f"dirty-{ rel_details.commit }"],
            build_args={}
        ),
        True
    )

    print(f":: Deploying {s.name} in { stage }...")
    if stage in configuration.stages.helm:
        helm_deploy(get_helm_main_release(s, rel_details, metadata))
    else:
        cf_deploy(get_cf_release_for_service(s, rel_details, metadata))

    print(f":: Deployed {s.name} in { stage }...")

@click.command("services/current", help="Check the metadata for current branch in the selected stage")
@click.option('--stage', '-e', help="Stage of the service", type=click.Choice(configuration.stages.all), default="dev")
@click.option('--service', '-s', help="Service to check", type=click.Choice(configuration.accepted_services), required=True)
def services_current(stage, service):
    s = ServiceResource(service)
    rel_details = ReleaseDetails(stage)
    metadata = ServiceReleaseMetadata()

    if stage in configuration.stages.helm:
        details = get_current_release_details(get_helm_main_release(s, rel_details, metadata), ServiceReleaseMetadata)
    else:
        details = cf_get_current_release_details(get_cf_release_for_service(s, rel_details, metadata), ServiceReleaseMetadata)

    print(f":: Current {s.name} in { stage }:")
    print(f"Releaser: { details.releaser }")
    print(f"Tag: { details.tag }")
    print(f"Dirty: { details.dirty }")
    print(f"Deploy date: { details.deploy_date }")
    print(f"Branch: { details.branch }")


@click.command("services/rollback", help="Rollback a service in the given stage")
@click.option('--stage', '-e', help="Stage of the service", type=click.Choice(configuration.stages.all), default="dev")
@click.option('--service', '-s', help="Service to rollback", type=click.Choice(configuration.accepted_services))
def services_rollback(stage, service):
    s = ServiceResource(service)
    rel_details = ReleaseDetails(stage)
    metadata = ServiceReleaseMetadata()

    if stage in configuration.stages.helm:
        helm_rollback(get_helm_main_release(s, rel_details, metadata))
    else:
        cf_rollback(get_cf_release_for_service(s, rel_details, metadata))



# @click.command("services/new", help="Create a new service")
# @click.option('--name', '-n', help="Name for the service", required=True)
# def services_new(name):
#     if 'hi.template' in configuration.services:
#         pass

#     if 'hi.' in name:
#         fullname = name
#         name = name.replace('hi.', '')
#     else:
#         fullname = f"hi.{ name }"

#     print(f":: Creating service under: { os.path.abspath(os.getcwd()) }")
#     shutil.copytree(configuration.services['hi.template'], f"./{ fullname }")
#     replace_in_file(f"./{ fullname }/package.json", "hi.template", fullname)
#     replace_in_file(f"./{ fullname }/src/index.ts", "hi.template", fullname)
#     replace_in_file(f"./{ fullname }/deployment/cloudformation.yaml", "template", name)
#     print("Done. Don't forget to add it to gitlab-ci.yml")


@click.command("services/logs", help="Check logs of a service")
@click.option('--stage', '-e', help="Stage of the service", type=click.Choice(configuration.stages.all), default="dev")
@click.option('--service', '-s', help="Service to check the logs of", type=click.Choice(configuration.accepted_services), required=True)
@click.option('--tail', '-t', help="Sets the logs to be tailed", default=False, is_flag=True)
@click.option('--milliseconds', '-ms', help="Show logs since the specified amount of milliseconds; default is 60000ms (1min)", default=60000)
def services_logs(stage, service, tail, milliseconds):
    s = ServiceResource(service)
    rel_details = ReleaseDetails(stage, releases="main")
    metadata = ServiceReleaseMetadata()

    if stage in configuration.stages.helm:
        release = get_helm_main_release(s, rel_details, metadata)
    else:
        release = get_cf_release_for_service(s, rel_details, metadata)

    print(f":: Logs for {s.name} in { stage }:")
    pod = get_pod_list_by_label(release.name, stage)[0]
    logs_for_pod(pod, stage, tail, milliseconds)


@click.command("services/remove", help="Remove a service")
@click.option('--service', '-s', type=click.Choice(configuration.accepted_services), help="Service to remove", required=True)
@click.option('--stage', '-e', type=click.Choice(configuration.stages.all), help="The stage of the service to remove")
@click.option('--confirm', prompt="You're about to remove a service. Recovery from this will need manual input (y/N)", help='Confirm whether you want to delete', default="N")
def services_remove(stage, service, confirm):
    if confirm.lower() not in [ "y", "yes"]:
        print("Aborting")
        exit(0)
    
    s = ServiceResource(service)
    rel_details = ReleaseDetails(stage)
    metadata = ServiceReleaseMetadata()

    print(f":: Removing {s.name} in { stage }")

    if stage in configuration.stages.helm:
        helm_remove(get_helm_main_release(s, rel_details, metadata))
    else:
        cf_remove(get_cf_release_for_service(s, rel_details, metadata))
    print(f":: Removed {s.name} in { stage }")

# @click.command("services/pipeline", help="Execute a gitlab pipeline for a service")
# @click.option('--stage', '-e', help="Stage to build for", type=click.Choice(configuration.stages.all), required=True)
# @click.option('--branch', '-b', help="Branch of this image")
# @click.option('--service', '-s', type=click.Choice(configuration.accepted_services), help="Service to build")
# def services_pipeline(stage, service, branch):
#     s = ServiceResource(service)

#     trigger_pipeline(s.repo.get_project(), branch or s.repo.get_branch(), {
#         "FORCE_BUILD": s.name,
#         "STAGE": s.stage
#     })

@click.command("services/docker", help="Build a docker image for a service")
@click.option('--stage', '-e', help="Stage to build for", default="dev")
@click.option('--remote', '-r', help="Build remotely", is_flag=True)
@click.option('--commit', '-c', help="Commit to use as tag")
@click.option('--push/--no-push', help="Whether to push the image or not", default=True)
@click.option('--npm/--no-npm', help="Whether to run npm build before docker build", default=True)
@click.option('--dirty/--not-dirty', help="Whether this build is dirty", default=True)
@click.option('--service', '-s', type=click.Choice(configuration.accepted_services), help="Service to build")
@click.option('--tags', '-t', help="csv of tags to buid, defaults to the commit tag")
def services_docker(stage, remote, service, tags, commit, push, npm, dirty):
    s = ServiceResource(service)

    if npm:
        npm_build(s.path)
        print(f":: NPM build finished. Building docker image for { s.name } in { stage }")

    commit = commit or GitRepo(s.path).get_commit()
    tags = [commit] + (tags.split(',') if tags else [])
    if dirty:
        tags.append(f"dirty-{ commit }")

    image = Image(
        s.name,
        s.path,
        get_valid_file(s.get_dockerfile_paths()),
        tags,
        build_args={}
    )

    if not remote:
        build_local(image, push)
    else:
        build_remote(image, push)

@click.command("services/template", help="Get the rendered helm values/cf stack for a service")
@click.option('--stage', '-e', help="Stage to template", type=click.Choice(configuration.stages.all), required=True)
@click.option('--service', '-s', type=click.Choice(configuration.accepted_services), help="Service to template")
@click.option('--image-tag', '-i', help="Image tag to use, defaults to the commit")
def services_template(stage, service, image_tag):
    s = ServiceResource(service)

    print(f":: Get template for { s.name } in { stage }")

    repo = GitRepo(s.path)
    rel_details = ReleaseDetails(
        stage,
        s.name,
        image_tag or repo.get_commit()
    )

    metadata = ServiceReleaseMetadata(
        repo.get_releaser(),
        repo.get_branch()
    )

    if stage in configuration.stages.helm:
        print(yaml.dump(get_helm_main_release(s, rel_details, metadata).values))
    else:
        print(yaml.dump(get_cf_release_for_service(s, rel_details, metadata).stack_template, Dumper=SafeUnknownDumper))

@click.command("services/history", help="Get the deployment history for a service")
@click.option('--stage', '-e', help="Stage of the service", type=click.Choice(configuration.stages.all), default="dev")
@click.option('--service', '-s', help="Service to check", type=click.Choice(configuration.accepted_services), required=True)
@click.option('--short', help="Do not collect metadata", is_flag = True, default = False)
def services_history(stage, service, short):
    s = ServiceResource(service)
    rel_details = ReleaseDetails(stage)
    metadata = ServiceReleaseMetadata()

    with_metadata = ServiceReleaseMetadata if not short else False
    if stage in configuration.stages.helm:
        history = helm_get_history(get_helm_main_release(s, rel_details, metadata), with_metadata=with_metadata)
    else:
        history = cf_get_history(get_cf_release_for_service(s, rel_details, metadata), with_metadata=with_metadata)

    if short:
        for h in history:
            print(h)
    else:
        for h in history:
            print(f"Releaser: { h.releaser }")
            print(f"Tag: { h.tag }")
            print(f"Dirty: { h.dirty }")
            print(f"Deploy date: { h.deploy_date }")
            print(f"Branch: { h.branch }")
            print("-------------------------------------")
