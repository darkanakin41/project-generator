from github import Github, GithubException

from generator.config import vcs_configuration, project_configuration
from generator.entity.project import Project
from tools.vcs.vcs_management import VCSManagement


class GitHubManagement(VCSManagement):
    """
    Github management functions
    """

    def __init__(self):
        super().__init__()
        self.configuration = vcs_configuration.get_type_configuration('github')
        self.vcs = Github(self.configuration.get('token'))

    @staticmethod
    def get_base_url():
        """
        Retrieve the base url
        :return:
        """
        return 'https://www.github.com'

    def get_repository_name(self, project: Project) -> str:
        """
        Retrieve the full repository name
        :param project: The project
        :return: the full repository name
        """
        user_name = self.configuration.get('user')
        return "{}/{}".format(user_name, project.name)

    def create_project(self, project: Project) -> str:
        """
        Create the right repository on github for the given project
        :param project: The project
        :return: the url
        """
        repository_name = self.get_repository_name(project)
        repo = None
        try:
            repo = self.vcs.get_repo(repository_name)
        except GithubException:
            pass

        user = self.vcs.get_user()
        if repo is None:
            repo = user.create_repo(project.name)
        repo.edit(description="This is a project generated using darkanakin41/project-generator",
                  private=True)

        return repo.ssh_url
