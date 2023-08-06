
import os
import click

from hi.engines.docker import build_local, build_remote
from hi.resources.image import Image


@click.command("docker/build", help="Build a docker image")
@click.option('--push/--no-push', help="Whether to push the image or not", default=True)
@click.option('--tags', '-t', help="csv of tags to buid, defaults to the commit tag")
@click.option('--remote', '-r', help="Build remotely", is_flag=True)
@click.option('--name', '-n', help="Name for the image", required=True)
@click.option('--arg', '-a', help="Arguments for the image", multiple=True)
def docker_build(name, remote, tags, push, arg):
    current_path = os.path.abspath(os.getcwd())
    arguments = {}
    for a in arg:
        spl = a.split('=')
        arguments[spl[0]] = '='.join(spl[1:])

    image = Image(name, current_path, f"{ current_path }/Dockerfile", None, tags.split(',') if tags else [], arguments)

    if not remote:
        build_local(image, push)
    else:
        build_remote(image, push)
