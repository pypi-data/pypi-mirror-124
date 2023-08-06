# hi.build

Manage services at hi.health

## Dependencies

kubectl
helm + s3 plugin
aws-google-auth
docker
python3

## Get started

1. Clone this repo:
```
git clone git@gitlab.dev.hi.health:platform/hi.cli.git
cd hi.cli
pip3 install .
```

2. Create the config file, scroll down to see the configuration.

3. Execute setup of tools if needed:
```
$ hi setup
Usage: hi setup [OPTIONS] COMMAND [ARGS]...

  Setup multiple tools to use this repo

Options:
  --help  Show this message and exit.

Commands:
  all
  aws-google-auth
  helm
  helmfile
  kubectl
```

4. Execute whatever you want:
```
$ hi
Usage: hi [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  aws/login                login to aws, provide access to cli and ecr
  aws/login/cli            login to aws cli
  aws/login/ecr            login to aws ecr
  charts/package           Package a chart to /tmp, so that it can be...
  charts/push              Push a chart in .tar.gz format to hi-charts repo
  charts/release           Package and push a chart to hi-charts repo
  cloudformation/deploy    Deploy a service to ECS
  cloudformation/remove    Remove a service from ECS
  cloudformation/template  Retrieve the cloudformation template for a...
  docker/build             Build a docker image
  gitlab/trigger           Trigger a pipeline
  helm/current             Get current deploy info for a service
  helm/deploy              Deploy a service via helm
  helm/remove              Remove a service from EKS
  helm/rollback            Rollback a service
  helm/template            Print the values file for a service in a stage
  serverless/deploy
  services/current         Check the metadata for current branch in the...
  services/deploy          Deploy to a service to a stage
  services/docker          Build a docker image for a service
  services/logs            Check logs of a service
  services/new             Create a new service
  services/release         Build and deploy a service
  services/remove          Remove a service
  services/rollback        Rollback a service in the given stage
  setup                    Setup multiple tools to use this repo
```

## Configuration

Configuration is written in TOML and placed in ~/.hi/config.
The following is a working example (modify user and repositories):
```
[aws]
user = "tiago.posse@hi.health"

  [aws.dev]
    default_profile = "default"
    default = "hi-dev-iam-role-base"

  [aws.prod]
    default_profile = "prod"
    prod = "hi-prod-iam-role-base"

[general]
repositories = [
  "/Users/tiagoposse/repos/backend/hi.services/hi.*",
  "/Users/tiagoposse/repos/apps/hi.*"
]
```

## Autocomplete

echo "eval \"$(_HI_COMPLETE=zsh_source hi)\"" >> ~/.zshrc
