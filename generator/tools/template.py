import os
import shutil
import stat
from distutils.dir_util import copy_tree

from git import Repo, Git

from generator.config.configuration import Configuration


class Template:
    """
    Template management
    """

    def __init__(self, project_type, template_name, template_path):
        self.project_type = project_type
        self.template_name = template_name
        self.template_path = template_path

    def copy(self, target_folder):
        """
        Copy the template into the target folder
        :param target_folder: the target folder
        :return:
        """
        if self.is_git_template():
            self._copy_git(target_folder)
        else:
            self._copy_directory(target_folder)

    def is_git_template(self):
        """
        Check if the template is a git repository or not
        :return:
        """
        return "git" in self.template_path or "https" in self.template_path

    def get_template_directory(self):
        """
        Calculate the template directory
        :return: the template directory
        """
        if self.is_git_template():
            return os.path.join(Configuration.get_template_directory(),
                                self.project_type,
                                self.template_name)
        return os.path.join(Configuration.get_template_directory(),
                            self.template_path)

    def _copy_directory(self, target_folder):
        """
        Copy the template folder into the target folder
        :param target_folder: the target folder
        :return:
        """
        print("[TEMPLATE] Copy files from '{}' to '{}'".format(self.get_template_directory(),
                                                               target_folder))
        copy_tree(self.get_template_directory(), target_folder)

    def _copy_git(self, target_folder):
        """
        Copy the git template into the target folder
        :param target_folder: the target folder
        :return:
        """
        template_directory = self.get_template_directory()

        if os.path.isdir(template_directory):
            print("[TEMPLATE] Updating template from git")
            Git(template_directory).pull()
        else:
            print("[TEMPLATE] Cloning template from git")
            Repo.clone_from(url=self.template_path, to_path=template_directory)

        self._copy_directory(target_folder)

        print("[TEMPLATE] Removal of .git folder coming from template")
        shutil.rmtree(os.path.join(target_folder, '.git'),
                      onerror=lambda func, path, exc_info: (os.chmod(path, stat.S_IWRITE), os.unlink(path)))
