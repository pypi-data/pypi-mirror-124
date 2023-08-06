import json
import os
import shutil
import yaml

from hi.utils.exec import run_command
from hi.utils.search import deep_merge, get_random_string, get_valid_file
from hi.resources import HelmRelease
from hi.resources.helm import HelmDeployment
from hi.resources.main import ReleaseDetails, ReleaseMetadata, Resource
from hi.engines.k8s import get_pod_list_by_label, get_secret_list, logs_for_pod

def add_repo(repository: dict):
    try:
        out = run_command(f"helm repo add { repository['name'] } { repository['url'] }")
        if 'already exists' not in out:
            run_command("helm repo update")
    except Exception as e:
        if 'already exists' in str(e):
            pass
        else:
            raise e


def deploy(release: HelmRelease, additionalArgs = {}):
    wait = '--wait' if release.wait else ''

    if release.chart_repo:
        add_repo(release.chart_repo)

    values_path = f"/tmp/helm-{ get_random_string(8) }/{ release.name }.yml"
    os.makedirs(os.path.dirname(values_path), exist_ok=True)

    with open(values_path, "w") as f:
        f.write(yaml.dump(release.values))

    overrides = " ".join([ f"--set {k}={v}" for k, v in additionalArgs.items()])

    # print(f"helm upgrade -i -n { stage } { r['name'] } { r['chart'] } --version { r['version'] } { wait } -f { values_path } { overrides }")
    run_command(' '.join([
        f"helm upgrade -i -n { release.namespace }",
        release.name,
        release.chart,
        f"--version { release.version }",
        wait,
        f"-f { values_path }",
        overrides
    ]))
    
    shutil.rmtree(os.path.dirname(values_path))

def remove(helm: HelmRelease):
    run_command(f"helm uninstall { helm.name } -n { helm.namespace } --wait")

def rollback(helm: HelmRelease):
    run_command(f"helm rollback { helm.name } -n { helm.namespace } --wait")


def template(helm: HelmRelease):
    return helm.values


def logs(helm: HelmRelease):
    pods = get_pod_list_by_label(helm.name, helm.namespace)
    print(logs_for_pod(pods[0], helm.namespace))


def read_values_for_revision(helm: HelmRelease, stage, revision = None):
    get_secret_list(stage, { 'fieldSelector': { 'type': 'helm.sh/release.v1' } })


def get_history(helm: HelmRelease, max: int = 50, with_metadata = None):
    history_resp = run_command(f"helm history { helm.name } -n { helm.namespace } --output json --max { max }")
    history = [ h for h in json.loads(history_resp) if h['description'] in ['Upgrade complete', 'Install complete'] ]

    if with_metadata:
        for i in range(len(history)):
            values = __get_values_for_release(helm.name, helm.namespace, revision=history[i]['revision'])
            metadata = with_metadata.metadata_from_helm_values(values)
            metadata.update({
                'tag': values['image']['tag'],
                'deploy_date': history[i]['updated']
            })
            history[i] = ReleaseMetadata(metadata)

    return history


def get_current_release_details(helm: HelmRelease, metadata_class):
    history = get_history(helm, max = 1)
    if not history:
        raise Exception(f"Couldn't get history for { helm.name } in { helm.namespace }. Something is really wrong with this deployment history.")

    h = history[-1]

    values = __get_values_for_release(helm.name, helm.namespace, revision=h['revision'])
    metadata = metadata_class.metadata_from_helm_values(values)
    metadata.update({
        'tag': values['image']['tag'],
        'deploy_date': h['updated']
    })
    return ReleaseMetadata(metadata)


def __get_values_for_release(release_name, stage, revision = 'latest'):
    if revision != 'latest':
        revision = f"--revision {revision}"
    else:
        revision = ""

    return json.loads(run_command(f"helm get values -n { stage } { release_name } --output json"))


def get_helm_main_release(service: Resource, details: ReleaseDetails, metadata: ReleaseMetadata = None):
    details.releases = 'main'
    return get_helm_releases_for_service(service, details, metadata)[0]

def get_helm_releases_for_service(service: Resource, details: ReleaseDetails, metadata: ReleaseMetadata):
    helm_deployment_file = get_valid_file(service.get_helmfile_paths())
    deployment = HelmDeployment.read_from_yaml_file(helm_deployment_file, { 'service': service, 'release': details, 'metadata': metadata })

    if details.releases == 'all':
        releases_to_deploy = list(deployment.releases.values())
    else:
        releases_to_deploy = []
        for r in details.releases.split(','):
            releases_to_deploy.append(deployment.releases[r])

    releases = []
    for r in releases_to_deploy:
        merged_stage = deep_merge(r.get('all'), r[details.stage])

        if merged_stage['chart'][0] in ['.', '/']: # it's a relative path
            chart_repo = {
                'name': os.path.basename(merged_stage['chart']),
                'url': os.path.dirname(merged_stage['chart'])
            }
        else: # it's a repo name
            chart_name = merged_stage['chart'].split('/')[0]
            chart_repo = {
                'name': chart_name,
                'url': deployment.repositories[chart_name]
            }
 
        releases.append(
            HelmRelease(
                merged_stage['name'],
                details.stage,
                merged_stage['chart'],
                merged_stage['version'],
                chart_repo,
                merged_stage['values']
            )
        )

    return releases
