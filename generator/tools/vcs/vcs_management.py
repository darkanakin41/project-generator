from abc import ABC, abstractmethod

from generator.config import project_configuration, vcs_configuration
from generator.entity.project import Project


class VCSManagement(ABC):
    """
    VCS Management Class
    """

    def __init__(self):
        self.vcs = None

    def get_gitignore_template(self, project: Project) -> str:
        """
        Retrieve the gitignore template for the given project
        :param project: The project
        :return: the content of the gitignore
        """
        gitignore_template = project_configuration.get_gitignore_template(project.type)
        gitignore_content = ''
        if gitignore_template is not None:
            gitignore_content += self.vcs.get_gitignore_template(gitignore_template).source
        if vcs_configuration.get_gitignore() is not None:
            if gitignore_content != '':
                gitignore_content += '\n'
            gitignore_content += '\n'.join(vcs_configuration.get_gitignore())
        return gitignore_content

    @staticmethod
    @abstractmethod
    def get_base_url() -> str:
        """
        Retrieve the base url
        :return:
        """
        pass

    @abstractmethod
    def get_repository_name(self, project: Project) -> str:
        """
        Retrieve the full repository name
        :param project: The project
        :return: the full repository name
        """
        pass

    @abstractmethod
    def create_project(self, project: Project) -> str:
        """
        Create the right repository for the given project
        :param project: The project
        :return: the url
        """
        pass
