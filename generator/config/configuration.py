import os
import sys

import yaml


class Configuration:
    """
    Management of the configuration file
    """

    @staticmethod
    def __base_folder__():
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    def __init__(self):
        self.config = None
        config_file = os.path.join(Configuration.__base_folder__(), "config.yaml")
        with open(config_file, "r") as stream:
            try:
                self.config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        if self.config is None:
            print("Please provide the right configuration")
            sys.exit()

    @staticmethod
    def get_template_directory():
        """
        Retrieve the template directory
        :return:
        """
        return os.path.join(Configuration.__base_folder__(), "templates")
