from setuptools import setup

setup(
    name='geovalidation.server',
    version='0.1',
    long_description="Flask-based server to validate GIS datasets (with prepair and val3dity).",
    packages=['geovalidation'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[	'Flask>=0.10.1'
						,'Jinja2>=2.7.2'
						,'Werkzeug>=0.9.4'
						,'celery>=3.1.11'
                        ,'redis>=2.9.1'
						,'lxml>=3.3.3'
						,'subprocess32>=3.2.6'
	author='Hugo Ledoux',
    author_email='h.ledoux@tudelft.nl'
)