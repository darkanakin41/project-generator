#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import webbrowser

from entity.project import Project
from tools.gitHubManagement import GitHubManagement

parser = argparse.ArgumentParser()
parser.add_argument("name", help="The name of the project you want to create")
parser.add_argument("--type", help="The name of the project you want to create  (default: default)", default="default")
parser.add_argument("--vcs", help="The version control system to use")
parser.add_argument("--template", help="The template to copy (default: default)", default="default")
args = parser.parse_args()

project_name = args.name
project_type = 'default'
vcs_type = None
if args.type:
    project_type = args.type
if args.vcs:
    vcs_type = args.vcs

project = Project(project_name, project_type)
project.create_dirs()
project.copy_template(args.template)

if vcs_type is not None:
    if project.is_vcs_initialized():
        print('VCS initialized')
    else:
        print('VCS not initialized')

if vcs_type == 'github':
    github = GitHubManagement()
    repo_url = github.create_project(project)
    repo_name = github.get_repository_name(project)
    gitignore_content = github.get_gitignore_template(project)
    if gitignore_content is not None:
        project.add_file('.gitignore', gitignore_content)

    project.add_file('README.md', '\n'.join([
        repo_name,
        '===',
        'This project have been generated with [darkanakin41/project-generator](https://github.com/darkanakin41/project-generator)'
    ]))

    project.init_git(repo_url)
    webbrowser.open('/'.join([
        github.get_base_url(),
        repo_name
    ]))

project.exec_commands()
