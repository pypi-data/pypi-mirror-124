
import requests

from hi.utils.exec import run_command
from hi.config.config import configuration


def trigger_pipeline(project, branch = None, additionalParams = {}):
    params = {
        "ref": branch,
    }

    for k, v in additionalParams.items():
        params[f"VARIABLES[{ k }]"] = v
    resp = requests.post(
        f"{ configuration.gitlab.address }/projects/{ project.replace('/', '%2F') }/pipeline",
        json=params,
        headers=configuration.gitlab.headers
    )
    print(resp.content)
