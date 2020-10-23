from generator.tools.vcs.github_management import GitHubManagement


class VCSFactory:
    """
    The factory for retrieving the right vcs
    """

    @staticmethod
    def get_management_for(vcs_type: str):
        """
        Get the right manager for the given vcs_type
        :param vcs_type: the VCS Type
        :return: VCSManagement
        """
        if vcs_type == 'github':
            return GitHubManagement()
        return None
