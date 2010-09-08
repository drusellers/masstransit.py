import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.rst')

setup(
    name = "masstransit-py",
    version = "0.0.1beta",
    url = 'http://github.com/drusellers/masstransit.py',
    license = 'Apache 2',
    description = "An attempt to have a basic port of MassTransit to python",
    long_description = README,
    author = 'Dru Sellers',
    author_email = 'dru@drusellers.com',
    install_requires = ['amqplib'],
    packages = [
        'masstransit',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: MassTransit',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache 2',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: AMQP',
    ]
)
