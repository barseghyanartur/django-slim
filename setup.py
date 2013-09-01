import os
from setuptools import setup, find_packages

try:
  readme = open(os.path.join(os.path.dirname(__file__), 'readme.rst')).read()
except:
  readme = ''

version = '0.5'

setup(
    name='django-slim',
    version=version,
    description=("Simple implementation of multi-lingual models for Django."),
    long_description=readme,
    classifiers=[
        "Programming Language :: Python",
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords='multi-lingual, django, python',
    author='Artur Barseghyan',
    author_email='artur.barseghyan@gmail.com',
    package_dir={'':'src'},
    packages=find_packages(where='./src'),
    url='https://bitbucket.org/barseghyanartur/django-slim',
    license='GPL 2.0/LGPL 2.1',
    install_requires = [
        #'Django>=1.5',
        'django-localeurl==1.5'
    ]
)
