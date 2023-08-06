import click

from hi.config.config import configuration
from hi.engines.gitlab import trigger_pipeline
from hi.resources.service import ServiceResource


@click.command('gitlab/trigger', help="Trigger a pipeline")
@click.option('--stage', '-e', type=click.Choice(configuration.stages.helm), help="Stage to trigger")
@click.option('--service', '-s', type=click.Choice(configuration.accepted_services), help="Service to trigger")
def gitlab_trigger_pipeline(stage, service):
    s = ServiceResource(service)
    trigger_pipeline(s)

@click.command('gitlab/cancel')
def gitlab_cancel_pipeline():
    pass
