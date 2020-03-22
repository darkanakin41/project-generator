from Config.Configuration import Configuration


class VCSConfiguration(Configuration):

    def __init__(self):
        super().__init__()
        if self.config.get('vcs') is None:
            print("Please provide the vcs configuration")
            exit()

    def get_configuration(self):
        """
        Get the vcs configuration from the configuration file
        :return: dict
        """
        return self.config.get('vcs')

    def get_type_configuration(self, vcs_type):
        """
        Get the configuration from the vcs type
        :param vcs_type: the type of vcs
        :return: dict
        """

        if self.get_configuration().get(vcs_type) is None:
            print("vcs.{} is missing from configuration file".format(vcs_type))
            exit()
        return self.get_configuration().get(vcs_type)

    def get_gitignore(self):
        """
        Get the gitignore
        :return: dict
        """
        gitignore = self.get_configuration().get('gitignore')
        if gitignore is None:
            print("vcs.{} is missing from configuration file".format('gitignore'))
            exit()
        return gitignore
