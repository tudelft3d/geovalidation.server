
# geovalidation.server

[Flask-based](http://flask.pocoo.org) server for some of our geovalidation tools:

1. [val3dity](https://github.com/tudelft3d/val3dity)
1. [prepair](https://github.com/tudelft3d/prepair)

These 2 should be installed and compiled, also the python scripts inside `val3dity/resources/...` are used (to convert GML to another format.)

## Installation

The recommended way to install the geovalidation server is using `virtualenv` and `pip`. 
Assuming you have working python (3.7+) installation with these utilities, run these commands:

```
virtualenv venv
source venv/bin/activate
pip install git+https://github.com/tudelft3d/geovalidation.server.git
```

Edit the configuration file `geovalidation.cfg` for you server and export them:

`export GEOVALIDATION_SETTINGS=/path/to/geovalidation.cfg`


## Folders to store (temporary) results and uploaded files

```
cd val3dity
mkdir uploads
mkdir reports
```


## Running the server

```
python runserver.py
```

Although for production use, you should use a proper WSGI server such as gunicorn.

