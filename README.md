Fabric-Deployer
===============

Repository for housing Dun & Bradstreet's Fabric file for PHP Deploys

# Getting Started #

_Add dandb/fabric-deployer to your composer.json file and copy fabfile to root of project after update_

__Inside: [project_root]/composer.json__

``` javascript
{
    "require": {
        "dandb/fabric-deployer": "*"
    },
    "repositories": [
        {   
            "type": "package",
            "package": {
                "name": "dandb/fabric-deployer",
                "version": "master",
                "source": {
                    "url": "git@github.com:dandb/fabric-deployer.git",
                    "type": "git",
                    "reference": "master"
                }   
            }   
        }   
    ],
    "scripts": {
        "post-update-cmd": [
            "cp vendor/dandb/fabric-deployer/src/fabfile.py fabric-lib.py"
        ]
    }
}
```

_Generate a 'config.json' file containing the mapping of environment to  URL inside your root project directory_

__Inside: [project_root]/fabric-config.json__

``` javascript
{
    "env": "https://env-site.com",
    "qa": "https://qa-site.com",
    "stg": "https://stg-site.com",
    "prd": "https://site.com"
}
```

_Add the following fabfile inside your root project directory_

__Inside: [project_root]/fabfile.py__

``` python
from fabric-lib import *

# If your project requires modifications to the fabric file, place them here. 
# def deploy():
```
