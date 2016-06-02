#!/usr/bin/env python
from setuptools import find_packages, setup
import os
import re


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = \'([0-9.]+)\'''')


def get_version():
    init = open(os.path.join(ROOT, 'application', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='groceries-api',
    version=get_version(),
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'alembic==0.7.5.post2',
        'APScheduler==3.1.0',
        'Flask==0.10.1',
        'Flask-Cors==2.0.0',
        'Flask-SQLAlchemy==2.0',
        'gunicorn==19.3.0',
        'psycopg2==2.6.1',
        'PyJWT==1.1.0',
        'six==1.9.0',
    ],
    extras_require={
        'dev': {
            'coverage==3.7.1',
            'coveralls==0.5',
            'flake8==2.4.0',
            'mock==1.0.1',
            'pytest==2.7.0',
            'tox==2.1.1',
        },
    },
)
