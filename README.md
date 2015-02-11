geovalidation
=============

code for [web server](http://geovalidation.bk.tudelft.nl) hosting val3dity

1. redis-server
2. celery -A val3dity.celery worker
3. python runserver.py