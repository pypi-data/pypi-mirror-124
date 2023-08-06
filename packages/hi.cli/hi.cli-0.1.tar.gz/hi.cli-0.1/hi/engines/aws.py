import subprocess
import base64
import boto3

from hi.config import configuration
from hi.utils.exec import run_command, run_stream_command

stages = {
    'dev': {
        'account': '272371606098',
        'default_role': 'hi-dev-iam-role-admin'
    },
    'prod': {
        'account': '873800019298',
        'default_role': 'hi-prod-iam-role-admin'
    }
}


def login_cli(stage, profile):
    conf_stage = getattr(configuration.aws, stage)
    print(conf_stage)
    role = conf_stage[conf_stage['default_profile']] if conf_stage.get('default_profile') else stages[stage]['default_role']
    profile = profile or conf_stage['default_profile'] or 'default'

    # print(f"aws-google-auth -I C017jong1 -S 1092969867109 -u { configuration['aws']['user'] } -R eu-central-1 -r arn:aws:iam::{ stages[stage]['account'] }:role/{ stages[stage]['role'] } -p { configuration['aws'][stage]['profile'] }")
    run_stream_command(f"aws-google-auth -I C017jong1 -S 1092969867109 -u { configuration.aws.user } -R eu-central-1 -r arn:aws:iam::{ stages[stage]['account'] }:role/{ role } -p { profile }")
    # print(subprocess.run(f"aws-google-auth -I C017jong1 -S 1092969867109 -u { configuration.aws.user } -R eu-central-1 -r arn:aws:iam::{ stages[stage]['account'] }:role/{ role } -p { profile }".split(), capture_output=True, shell=True).stdout.decode().strip())

def login_ecr():
    client = boto3.client('ecr')
    response = client.get_authorization_token()
    password = base64.b64decode(response['authorizationData'][0]['authorizationToken']).decode()[4:]
    
    print(subprocess.run(f"docker login --username AWS --password=\"{ password }\" 272371606098.dkr.ecr.eu-central-1.amazonaws.com", capture_output=True, shell=True).stdout.decode().strip())


def read_values_for_revision():
    pass

def read_values_for_history():
    pass
