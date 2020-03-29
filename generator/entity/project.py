import os
import pathlib
from distutils.dir_util import copy_tree

from config import projectConfiguration
from git import Repo, InvalidGitRepositoryError


class Project:

    def __init__(self, name, project_type):
        self.name = name
        self.type = project_type
        self.repo_url = None

    def set_repo_url(self, repo_url):
        """
        Define the repo_url of the folder
        :param repo_url: the url of the repository
        :return:
        """
        self.repo_url = repo_url

    def get_project_dir(self):
        """
        Retrieve the base project folder dir from the configuration
        :return: string the folder
        """
        return projectConfiguration.get_folder(self.name, self.type)

    def create_dirs(self):
        """
        Create the needed directories if needed
        :return:
        """
        project_dir = self.get_project_dir()
        if os.path.isdir(project_dir):
            print("[BASE] Project already exists")
        else:
            pathlib.Path(project_dir).mkdir(parents=True, exist_ok=True)
            print("[BASE] Project folder '{}' created".format(project_dir))

    def exec_commands(self):
        """
        Execute the commands
        :return: void
        """
        commands = projectConfiguration.get_exec_command(self.type)
        if commands is not None and isinstance(commands, str):
            self._exec_command(commands)
        elif commands is not None and isinstance(commands, list):
            for command in commands:
                self._exec_command(command)
        else:
            print("[BASE] No command to execute")

    def _exec_command(self, command):
        """
        Execute the command
        :param command: execute the given command in the project folder
        :return:
        """
        project_dir = self.get_project_dir()
        print("[BASE] Execution of {}".format(command))
        os.system("{} {}".format(command, project_dir))

    def is_vcs_initialized(self):
        """
        Check if the .git repository exist
        :return:
        """
        project_dir = self.get_project_dir()
        return os.path.isdir(os.path.join(project_dir, '.git'))

    def add_file(self, filename, content):
        """
        Create the given filename in the folder with given content
        :param filename: the name of the file to create
        :param content: the content of the file
        :return:
        """
        project_dir = self.get_project_dir()

        with open(os.path.join(project_dir, filename), "w") as stream:
            stream.write(content)

    def init_git(self, repo_url):
        """
        Init the git repository in the folder
        :param repo_url: the url of the repository
        :return:
        """
        try:
            repo = Repo(self.get_project_dir())
            print('[GIT] This is already a git repository')
            return
        except InvalidGitRepositoryError as exc:
            repo = Repo.init(self.get_project_dir())
            print('[GIT] git init the repository')

        try:
            origin = repo.remote('origin')
            print('[GIT] Retrieving the origin remote')
        except ValueError as exc:
            origin = repo.create_remote('origin', repo_url)
            print('[GIT] Adding the remote "origin" : {}'.format(repo_url))

        if len(repo.untracked_files) > 0:
            repo.git.add('.')
            print('[GIT] Staging new files')
        if repo.is_dirty():
            print('[GIT] Initial commit')
            repo.git.commit('-m "Initial commit"')
            print('[GIT] Pushing files to remote')
            repo.git.push("--set-upstream", origin, repo.head.ref)

    def copy_template(self, template_name):
        """
        Copy the given template into the folder
        :param template_name: the name of the template
        :return: void
        """
        files = os.listdir(self.get_project_dir())
        if len(files) > 0:
            print("[TEMPLATE] Unable to copy template because project is already initialized")
            return

        template = projectConfiguration.get_template(self.type, template_name)

        if template is None:
            print("[TEMPLATE] {} is not defined in {} configuration".format(template_name, self.type))
            return

        template.copy(self.get_project_dir())
