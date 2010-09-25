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
    description = "A port of the .Net MassTransit ESB to python. But with more awesome",
    long_description = README,
    author = 'Dru Sellers',
    author_email = 'dru@drusellers.com',
    install_requires = ['amqplib','gevent'],
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
