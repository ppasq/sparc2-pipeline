# SPARC 2.x Pipeline (sparc2-pipeline)

Data pipeline tools for importing & exporting data in the SPARC 2.x platform.  Uses [Fabric](http://www.fabfile.org/) to transfer files and [python-cli-util](https://github.com/pjdufour/python-cli-util) for command-line interaction.

# Installation

On the control/host machine, you'll need to install [Fabric](http://www.fabfile.org).

**Quick Install**

To quickly install [Fabric](http://www.fabfile.org) to system python, run the following:

```
sudo apt-get install python-dev # if not already installed
sudo easy_install pip  # if pip is not already installed
sudo pip install virtualenv virtualenvwrapper
# cd into project directory
sudo pip install -r requirements.txt
```

On the other hand, if you wish to use a python virtual environment on your host/control machine, be sure to install `virutalenv` and `virtualenvwrapper`.  Your `~/.bash_aliases` file should look something like the following:

```
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
export WORKON_HOME=~/.venvs
source /usr/local/bin/virtualenvwrapper.sh
export PIP_DOWNLOAD_CACHE=$HOME/.pip-downloads
```

## Fabric

[Fabric](http://www.fabfile.org/) provides an easy command line interface for executing remote shell commands and for transferring files between machines.  Fabric is extremely useful for transferring files and managing remote servers.

Follow directions at http://www.fabfile.org/installing.html to install fabric or follow shortcuts below.

#### Mac OS X & Ubuntu

```
sudo pip install fabric
```

# Configuration

Before you run pipeline commands, such as `shp`, `sql`, etc. you'll need to set up your target environment configurations and add the command to load the configuration to your fabfile.py.  The fab commands for `prod` (for production) and `dev` (for development) are already in the fabfile.py.  You'll need to add the configurations to `env/prod.yml` and `env/dev.yml`.  For example, here is the configuration for a local vagrant development machine.

```
---
disable_known_hosts: True
hosts:
  - localhost:2222
user: vagrant
group: vagrant
password:
key_filename: "~/workspaces/public/sparc2-ansible.git/.vagrant/machines/default/virtualbox/private_key"

sparc2:
  user: vagrant
  venv: "/home/vagrant/.venvs/sparc2"
  db:
    host: localhost
    name: sparc2
    user: sparc2
    password: sparc2

```

# Usage

## Fabric

[Fabric](http://www.fabfile.org/) provides an easy command line interface for executing remote shell commands and for transferring files between machines.  For SPARC 2.x, Fabric can be used to import and export data.

To get started, change directory (`cd`) into the main directory with the `fabfile.py`.  When you call fab, start with `dev` or `prod` so that the host and identity key are loaded automatically.


To see a list of tasks run:

```
fab -l
```

To see the long description of a task run:

```
fab -d taskname
```

A few examples:

```
fab dev lsb_release
fab dev pipeline_sql_clear:tables="cyclone.events;drought.events",sep=";"
fab dev pipeline_sql_schemas:schemas="cyclone;flood;drought",sep=";"
fab dev shp:drop=/opt/drop,geometry_type=MULTIPOLYGON,op=replace,local_path=$LOCAL_PATH,table=$TABLE
fab dev sql:drop=/opt/drop,local_path="foo.sql"
fab dev copy:src="foo/bar.*",dest=/opt/drop
```


For example, importing GAUL Admin 0 polygons:

```
TARGET=dev
OP=replace
TYPE="MULTIPOLYGON"
TABLE="gaul.admin0_polygons"
LOCAL_PATH="~/data/sparc/sparc2/gaul2015/wld_bnd_adm0_gaul_2015.*"
fab $TARGET \
shp:drop=$DROP,geometry_type=$TYPE,op=$OP,local_path=$LOCAL_PATH,table=$TABLE
```
