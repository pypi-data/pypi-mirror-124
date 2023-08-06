import click

from hi.engines.setup import helm, kubectl, aws_google_auth


@click.command("setup/all", help="Setup multiple tools to use this repo")
def setup_all():
    aws_google_auth()
    kubectl()
    helm()

@click.command("setup/helm", help="Setup helm in the system")
def setup_helm():
    helm()

@click.command("setup/kubectl", help="Setup kubectl")
def setup_kubectl():
    kubectl()

@click.command("setup/aws-google-auth",  help="Setup aws-google-auth")
def setup_aws_google_auth():
    aws_google_auth()
