from github import Github, GithubException

from generator.config import vcsConfiguration, projectConfiguration
from generator.entity.project import Project


class GitHubManagement:

    def __init__(self):
        self.configuration = vcsConfiguration.get_type_configuration('github')
        self.vcs = Github(self.configuration.get('token'))

    def get_base_url(self):
        return 'https://www.github.com'

    def get_repository_name(self, project: Project):
        user_name = self.configuration.get('user')
        return "{}/{}".format(user_name, project.name)

    def create_project(self, project: Project):
        repository_name = self.get_repository_name(project)
        repo = None
        try:
            repo = self.vcs.get_repo(repository_name)
            # return repo
        except GithubException as exc:
            pass

        user = self.vcs.get_user()
        if repo is None:
            repo = user.create_repo(project.name)
        repo.edit(description="This is a project generated using darkanakin41/project-management", private=True)

        return repo.ssh_url

    def get_gitignore_template(self, project: Project):
        gitignore_template = projectConfiguration.get_gitignore_template(project.type)
        gitignore_content = ''
        if gitignore_template is not None:
            gitignore_content += self.vcs.get_gitignore_template(gitignore_template).source
        if vcsConfiguration.get_gitignore() is not None:
            if gitignore_content != '':
                gitignore_content += '\n'
            gitignore_content += '\n'.join(vcsConfiguration.get_gitignore())
        return gitignore_content
