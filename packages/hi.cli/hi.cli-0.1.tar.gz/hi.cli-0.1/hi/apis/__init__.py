
from hi.config import configuration
import hi.apis.aws_api as aws_api
import hi.apis.cloudformation_api as cloudformation_api
import hi.apis.docker_api as docker_api
# import hi.apis.gitlab_api as gitlab_api
import hi.apis.services_api as services_api
import hi.apis.setup_api as setup_api
import hi.apis.helm_api as helm_api

def get_apis(debug = False):
    apis = [
        aws_api,
        services_api,
        setup_api,
        docker_api
    ]

    if configuration.infra:
        import hi.apis.infra_api as infra_api
        apis.append(infra_api)

    if debug:
        apis += [
            helm_api,
            cloudformation_api
        ]

    return apis
