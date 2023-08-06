import click

from hi.config import configuration
from hi.engines.aws import login_cli, login_ecr

@click.command("aws/login", help="login to aws, provide access to cli and ecr")
@click.option('--stage', '-s', help="Profile to authenticate to", type=click.Choice(['dev', 'prod']), default="dev")
@click.option('--profile', '-p', help="Profile to authenticate to", type=click.Choice(configuration.aws.get_profiles()))
def aws_login(stage, profile):
    login_cli(stage, profile)
    login_ecr()

@click.command("aws/login/cli", help="login to aws cli")
@click.option('--stage', '-s', help="Profile to authenticate to", type=click.Choice(['dev', 'prod']), default="dev")
@click.option('--profile', '-p', help="Profile to authenticate to", type=click.Choice(configuration.aws.get_profiles()))
def aws_login_cli(stage, profile):
    login_cli(stage, profile)

@click.command("aws/login/ecr", help="login to aws ecr")
def aws_login_ecr():
    login_ecr()
