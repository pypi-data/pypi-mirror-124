from hi.utils.exec import run_command

import re

class GitRepo:
    def __init__(self, context):
        self.commit = None
        self.branch = None
        self.releaser = None
        self.project = None
        self.context = context

    def get_commit(self):
        self.commit = self.commit or run_command(f"cd { self.context }; git log --format=%H -n 1")
        return self.commit

    def get_releaser(self):
        self.releaser = self.releaser or run_command(f"cd { self.context }; git config --get user.email")
        return self.releaser

    def get_branch(self):
        self.branch = self.branch or run_command(f"cd { self.context }; git branch --show-current")
        return self.branch

    def get_project(self):
        if not self.project:
            project_url = run_command(f"cd { self.context }; git config --get remote.origin.url")
            matches = re.search('.+?:((?:\w+)/(?:.+?)).git', project_url)
            self.project = matches.group(1)

        return self.project
