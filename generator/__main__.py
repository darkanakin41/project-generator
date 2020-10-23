#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import webbrowser
from typing import Optional, Sequence

from generator.entity.project import Project
from generator.tools.vcs.github_management import GitHubManagement
from generator.tools.vcs_factory import VCSFactory

parser = argparse.ArgumentParser()
parser.add_argument("name",
                    help="The name of the project you want to create")
parser.add_argument("--type",
                    help="The name of the project you want to create (default: default)",
                    default="default")
parser.add_argument("--vcs",
                    help="The version control system to use")
parser.add_argument("--template",
                    help="The template to copy (default: default)",
                    default="default")


def main(args: Optional[Sequence[str]] = None):
    """
    Process the command
    :param args:
    :return:
    """
    arguments = parser.parse_args(args)

    project_name = arguments.name
    project_type = 'default'
    vcs_type = None
    repo_url = None
    vcs = None
    if arguments.type:
        project_type = arguments.type
    if arguments.vcs:
        vcs_type = arguments.vcs

    project = Project(project_name, project_type)
    project.create_dirs()
    project.copy_template(arguments.template)

    if vcs_type is not None:
        vcs = VCSFactory.get_management_for(vcs_type)
        if project.is_vcs_initialized():
            print('[VCS] Initialized')
        else:
            print('[VCS] Initializing')
            project.is_vcs_initialized()

    if vcs is not None:
        repo_url = vcs.create_project(project)
        repo_name = vcs.get_repository_name(project)
        gitignore_content = vcs.get_gitignore_template(project)
        if gitignore_content is not None:
            project.add_file('.gitignore', gitignore_content)

        project.add_file('README.md', '\n'.join([
            repo_name,
            '===',
            'This project have been generated with [darkanakin41/project-generator]'
            '(https://github.com/darkanakin41/project-generator)'
        ]))

        webbrowser.open('/'.join([
            GitHubManagement.get_base_url(),
            repo_name
        ]))

    project.init_git(repo_url)

    project.exec_commands()


def console_script():  # pragma: no cover
    """
    Console script entrypoint
    """
    main()
