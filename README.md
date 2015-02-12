geovalidation
=============

code for [web server](http://geovalidation.bk.tudelft.nl) hosting val3dity

1. redis-server
2. celery -A val3dity.celery worker
3. sqlite3 val3dity.sqlite < schema.sql
4. python runserver.py