
# geovalidation.server


[Flask-based](http://flask.pocoo.org) server for some of the geovalidation that we've built:

1. [val3dity](https://github.com/tudelft3d/val3dity)
1. [prepair](https://github.com/tudelft3d/prepair)


## Installation

First, [Redis](http://redis.io) must be installed.

The recommended way to install the server is using `virtualenv` and `pip`. 
Assuming you have working python (2.7.x) installation with these utilities, run these commands:

```
virtualenv venv
source venv/bin/activate
pip install git+https://github.com/tudelft3d/geovalidation.server.git
```

Now you need to create a MATAHN configuration file for you server:

```
wget https://raw.githubusercontent.com/tudelft3d/matahn/master/example_matahn.cfg
mv example_matahn.cfg matahn.cfg
``


1. redis-server
2. celery -A val3dity.celery worker
3. sqlite3 val3dity.sqlite < schema.sql
4. python runserver.py