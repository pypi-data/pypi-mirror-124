

from hi.config.config import configuration
from hi.resources.cloudformation import CFRelease
from hi.resources.helm import HelmRelease
from hi.resources.main import ReleaseDetails
from hi.resources.service import ServiceReleaseMetadata, ServiceResource
from hi.engines.helm import get_history as helm_get_history, get_current_release_details as helm_get_current_release_details, get_helm_main_release
from hi.engines.cloudformation import get_history as cf_get_history,  get_current_release_details as cf_get_current_release_details, get_cf_release_for_service



histories = {}

# def get_current_services():
#     for name, resource in histories:
#         get_latest_revision_number()


def get_current_service_release(service: ServiceResource):
    helm_get_current_release_details()
    cf_get_current_release_details


def get_history_for_service(service: ServiceResource, stage):
    if stage in configuration.stages.helm:
        release = HelmRelease(service.short_name, stage, None, None, None, None)
        helm_get_history(release, with_metadata=ServiceReleaseMetadata)
    else:
        cluster, container, task, stack = service.get_cf_details(stage)
        release = CFRelease(task, cluster, stack, container)
        cf_get_history(release, with_metadata=ServiceReleaseMetadata)



def get_current_release_for_services(services: list, stage):
    releases = []

    for service in services:
        s = ServiceResource(service)
        rel_details = ReleaseDetails(stage)
        metadata = ServiceReleaseMetadata()

        if stage in configuration.stages.helm:
            releases.append(helm_get_current_release_details(get_helm_main_release(s, rel_details, metadata), ServiceReleaseMetadata))
        else:
            releases(cf_get_current_release_details(get_cf_release_for_service(s, rel_details, metadata), ServiceReleaseMetadata))

    print(releases)
