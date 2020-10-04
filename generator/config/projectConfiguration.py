import os

from generator.config.configuration import Configuration
from generator.tools.template import Template


class ProjectConfiguration(Configuration):
    def __init__(self):
        super().__init__()
        if self.config.get('project') is None:
            print("Please provide the project configuration")
            exit()

    def get_configuration(self):
        """
        Get the project configuration from the configuration file
        :return: dict
        """
        return self.config.get('project')

    # CONFIGURATION READING METHODS

    def get_types_configuration(self):
        """
        Get the types configuration from the configuration file
        :return: dict
        """
        if self.get_configuration().get('types') is None:
            print("Please provide the project configuration")
            exit()
        return self.get_configuration().get('types')

    def get_type_configuration(self, project_type):
        """
        Get the type configuration from the configuration file
        :param project_type: the type to look for
        :return: dict
        """
        if self.get_types_configuration().get(project_type) is None:
            print("Type {} is missing in configuration".format(project_type))
            exit()
        return self.get_types_configuration().get(project_type)

    # UTILITIES METHODS

    def get_base_folder(self):
        """
        Get the global base project folder
        :return: string
        """
        if self.get_configuration().get('base_folder') is None:
            print("project.base_folder is missing from configuration file")
            exit()
        return self.config.get('project').get('base_folder')

    def get_folder(self, name, project_type):
        """
        Get the base project folder for given project name and type
        :param name: the name of the project
        :param project_type: the type of the project
        :return: string
        """
        project_type_folder = self.get_type_configuration(project_type).get('folder')
        if project_type_folder is None:
            print("project.folder is missing from configuration file")
            exit()

        return os.path.join(self.get_base_folder(), project_type_folder, name)

    def get_exec_command(self, project_type):
        """
        Get the command to execute after processing the project
        :param project_type: the type of the project
        :return: string
        """
        return self.get_type_configuration(project_type).get('exec')

    def get_gitignore_template(self, project_type):
        """
        Get the gitignore template
        :param project_type: the type of the project
        :return: string
        """
        return self.get_type_configuration(project_type).get('gitignore_template')

    def get_templates(self, project_type):
        """
        Get the gitignore template
        :param project_type: the type of the project
        :return: string
        """
        return self.get_type_configuration(project_type).get('templates')

    def get_template(self, project_type, template):
        """
        Get the gitignore template
        :param project_type: the type of the project
        :param template: the type of the project
        :return: Template | None
        """
        if self.get_type_configuration(project_type).get('templates') is None:
            return None
        template_configuration = self.get_type_configuration(project_type).get('templates').get(template)
        if template_configuration is None:
            return None
        return Template(project_type, template, template_configuration)
