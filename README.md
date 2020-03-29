darkanakin41/project-generator
===

This project is a toolbox to initialize project on the system. 

Based on config.yaml, it create the project in the right folder, can open your favorite IDE 
and even initialize the project on your version management system if you want to.

Currently, if well configured (see [config.yaml.dist](config.yaml.dist) for more details), it will : 
* Create the folder with the name of the project
* Copy a template if one is given
* Create the github repository
* Create a readme and a gitignore file in the repository
* Open the github project in your browser
* Execute a command such as open your IDE with the project

# Development
* Install requirements : 
```bash
pip install -r requirements-dev.txt
```

# Github Token Access
The token needs to have the full repo scop :
* repo:status
* repo:invite
* repo_deployment
* public_repo

# Usage
```bash
python generator --help
usage: generator [-h] [--type TYPE] [--vcs VCS] [--template TEMPLATE] name

positional arguments:
  name                 The name of the project you want to create

optional arguments:
  -h, --help           show this help message and exit
  --type TYPE          The name of the project you want to create (default: default)
  --vcs VCS            The version control system to use
  --template TEMPLATE  The template to copy (default: default)
```
