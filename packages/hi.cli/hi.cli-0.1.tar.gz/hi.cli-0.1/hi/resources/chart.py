import yaml
import os

from hi.utils.errors import ParamError
from hi.config import configuration


class Chart:
    """This object represents a Helm Chart

    Used by the Chart engine to describe helm charts managed through it. It is the accepted request parameter to charts api.

    Attributes
    ----------
    name : str
        the name of the chart
    version : str
        version of the chart
    path : str
        filesystem path to the chart, used to package and push
    """

    def __init__(self, name, version, path) -> None:
        self.name = name
        self.version = version
        self.path = path

    @classmethod
    def from_chart_yaml(cls, chart_path: str, chart: dict = {}):
        """Load a chart from a yaml"""

        path = Chart.get_chart_path(chart_path)
        if not chart:
            with open(f"{ path }/Chart.yaml", "r") as f:
                chart = yaml.safe_load(f.read())

        return Chart(
            chart['name'],
            chart['version'],
            path
        )

    @classmethod
    def get_chart_path(cls, chart: str = None):
        """ Get the filesystem path for a chart.

        Parameters
        ----------
        chart : str, optional
            The name of the chart. If not provided, the name is retrieved from cwd, if it exists as a chart in the system"""

        if not chart:
            path = os.getcwd()

            for p in path.split('/')[::-1]:
                if p in configuration.infra.accepted_charts:
                    return p

            raise ParamError(f"Service name not provided and unable to retrive from current path: { path }")

        if chart not in configuration.infra.accepted_charts:
            raise ParamError(f"Chart '{ chart }' is not currently supported")

        return configuration.infra.charts[chart]
