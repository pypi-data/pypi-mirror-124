import click
from hi.engines.charts import package, push
from hi.resources import Chart

@click.command('charts/package', help="Package a chart to /tmp, so that it can be pushed to a repo")
@click.option('--path', '-p', help="Path of the chart to package. Defaults to cwd", type=str)
def charts_package(path):
    package(Chart.from_chart_yaml(path))

@click.command('charts/release', help="Package and push a chart to hi-charts repo")
@click.option('--path', '-p', help="Path of the chart to release. Defaults to cwd", type=str)
def charts_release(path):
    if not path:
        path = "."

    chart = Chart.from_chart_yaml(path)
    package(chart)
    push(chart)
