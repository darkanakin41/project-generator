from .GitHubManagement import GitHubManagement


class VCSTools:
    @staticmethod
    def get_management_for(vcs_type):
        if vcs_type == 'github':
            return GitHubManagement()
