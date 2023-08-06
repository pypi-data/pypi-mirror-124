from hi.resources import Chart
from hi.utils.exec import run_command

def package(c: Chart):
    run_command(f'helm lint { c.path }')
    output = run_command(f'helm package { c.path } -d /tmp')

    c.download_path = output.split(':')[1][1:]


def push(c: Chart):
    run_command(f"helm s3 push { c.download_path } hi-charts")
