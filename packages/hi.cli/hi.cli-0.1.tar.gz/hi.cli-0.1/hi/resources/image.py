from hi.utils.errors import ParamError

class Image:
    """This object represents a Docker Image

    Used by the docker engine to know how to build and push images.

    Attributes
    ----------
    name : str
        name of the image
    context : str
        filesystem path to the context of the image
    dockerfile : str
        filesystem path to the dockerifle
    tags : list
        a list of tags for the image
    build_args : dict [optional]
        a dictionary containing build arguments for the image. Each pair will be passed as --build-arg={KEY}={VALUE}
    """

    def __init__(
            self,
            name: str,
            context: str,
            dockerfile: str,
            tags: list,
            build_args: dict = {}
        ):

        if not name:
            raise ParamError("Need to specify a name for this image")

        if not context:
            raise ParamError("Need to specify a context for this image")

        if not dockerfile:
            raise ParamError("Need to specify a dockerfile for this image")

        if not tags:
            raise ParamError("Need to specify at least one tag for this image")

        self.name = name
        self.context = context
        self.dockerfile = dockerfile
        self.tags = tags
        self.build_args = build_args

    def get_build_args_as_string(self):
        return ' '.join([ f"--build-arg={ key }={ val }" for key, val in self.build_args.items() ])
