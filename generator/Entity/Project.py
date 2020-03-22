import os
import pathlib

from Config import projectConfiguration
from git import Repo, InvalidGitRepositoryError, GitCommandError


class Project:

    def __init__(self, name, project_type):
        self.name = name
        self.type = project_type
        self.repo_url = None

    def set_repo_url(self, repo_url):
        self.repo_url = repo_url

    def get_project_dir(self):
        return projectConfiguration.get_folder(self.name, self.type)

    def create_dirs(self):
        project_dir = self.get_project_dir()
        if os.path.isdir(project_dir):
            print("Project already exists")
        else:
            pathlib.Path(project_dir).mkdir(parents=True, exist_ok=True)
            print("Project folder '{}' created".format(project_dir))

    def exec_command(self):
        project_dir = self.get_project_dir()
        command = projectConfiguration.get_exec_command(self.type)
        if command is not None:
            print("Execution of {}".format(command))
            os.system("{} {}".format(command, project_dir))

    def is_vcs_initialized(self):
        project_dir = self.get_project_dir()
        return os.path.isdir(os.path.join(project_dir, '.git'))

    def add_file(self, filename, content):
        project_dir = self.get_project_dir()

        with open(os.path.join(project_dir, filename), "w") as stream:
            stream.write(content)

    def init_git(self, repo_url):
        try:
            repo = Repo(self.get_project_dir())
            print('This is already a git repository')
            return
        except InvalidGitRepositoryError as exc:
            repo = Repo.init(self.get_project_dir())
            print('git init the repository')

        try:
            origin = repo.remote('origin')
            print('Retrieving the origin remote')
        except ValueError as exc:
            origin = repo.create_remote('origin', repo_url)
            print('Adding the remote "origin" : {}'.format(repo_url))

        # if repo.is_dirty():
        if len(repo.untracked_files) > 0:
            repo.git.add('.')
            print('Staging new files')
        if repo.is_dirty():
            print('Initial commit')
            repo.git.commit('-m "Initial commit"')
            print('Pushing files to remote')
            repo.git.push("--set-upstream", origin, repo.head.ref)
