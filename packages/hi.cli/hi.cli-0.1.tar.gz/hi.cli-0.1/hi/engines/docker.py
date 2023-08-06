import json

from hi.config import configuration
from hi.resources.image import Image
from hi.utils.exec import run_stream_command

def build_local(image: Image, push = True):
    __print_build_info(image)

    command = f"docker build --tag={ configuration.ecr_repository }/{ image.name }:{ image.tags[0] } --file={ image.dockerfile } { image.context }"
    b_args = image.get_build_args_as_string()
    if b_args:
        command += " " + b_args

    print(command)
    run_stream_command(command)

    if push:
        tagged_images = [ f"{ configuration.ecr_repository }/{ image.name }:{ tag }" for tag in image.tags ]
        print(f":: Push { tagged_images[0] }")
        run_stream_command(f"docker push { tagged_images[0] }")

        for t in tagged_images[1:]:
            print(f":: Push { t }")
            run_stream_command(f"docker tag { tagged_images[0] } { t }; docker push { t }")

    print(":: Docker build step finished.")

def build_remote(image, push = True):
    with open('/kaniko/.docker/config.json', 'w') as f:
        f.write(json.dumps({
            "credsStore": "ecr-login",
            "credHelpers": {
                configuration.ecr_repository: "ecr-login"
            }
        }))
    
    __print_build_info(image)
    
    tagged_images = ','.join([ f"--destination={ configuration.ecr_repository }/{ image.name }:{ tag }" for tag in image.tags ])

    command = f"/kaniko/executor -c { image.context } -f { image.dockerfile } { tagged_images } { image.get_build_args_as_string() }"
    if not push:
        command += "--no-push"

    print(command)
    run_stream_command(command)


def __print_build_info(image: Image):
    print(f"Context: { image.context }")
    print(f"Dockerfile: { image.dockerfile }")
    print(f"Repo: { configuration.ecr_repository }/{ image.name }")
    print(f"Tags: { ','.join(image.tags) }")
