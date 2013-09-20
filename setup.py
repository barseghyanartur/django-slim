import sys
import os
from setuptools import setup, find_packages

try:
  readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
  readme = ''

version = '0.7.1'

install_requires = [
    'six==1.4.1',
]

try:
    PY2 = sys.version_info[0] == 2
    PY3 = sys.version_info[0] == 3
    if PY2:
        install_requires.append('django-localeurl==2.0.1')
except:
    pass

setup(
    name = 'django-slim',
    version = version,
    description = ("Simple implementation of multi-lingual models for Django."),
    long_description = readme,
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
    ],
    keywords = 'multi-lingual, django, python',
    author = 'Artur Barseghyan',
    author_email = 'artur.barseghyan@gmail.com',
    package_dir = {'':'src'},
    packages = find_packages(where='./src'),
    url = 'https://bitbucket.org/barseghyanartur/django-slim',
    license = 'GPL 2.0/LGPL 2.1',
    install_requires = install_requires
)
