
# geovalidation.server


[Flask-based](http://flask.pocoo.org) server for some of our geovalidation tools:

1. [val3dity](https://github.com/tudelft3d/val3dity)
1. [prepair](https://github.com/tudelft3d/prepair)

These 2 should be installed and compiled, also the python scripts inside `val3dity/resources/...` are used (to convert GML to another format.)

## Installation

First, [Redis](http://redis.io) must be installed.

The recommended way to install the geovalidation server is using `virtualenv` and `pip`. 
Assuming you have working python (2.7.x) installation with these utilities, run these commands:

```
virtualenv venv
source venv/bin/activate
pip install git+https://github.com/tudelft3d/geovalidation.server.git
```

Edit the configuration file `geovalidation.cfg` for you server and export them:

`export GEOVALIDATION_SETTINGS=/path/to/geovalidation.cfg`


## sqlite database

A small database (`val3dity.sql`) must be used to store the results:

`sqlite3 val3dity.sqlite < schema.sql`


## Running the server

```
redis-server
celery -A val3dity.celery worker
python runserver.py
```

Although for production use, you should use a proper WSGI server such as gunicorn.

