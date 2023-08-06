
class Error(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message

class DockerBuildError(Error):
    pass

class ParamError(Error):
    pass

class ExecError(Error):
    pass
