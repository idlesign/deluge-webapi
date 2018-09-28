import os
from setuptools import setup
from webapi import VERSION


PATH_BASE = os.path.dirname(__file__)
PATH_BIN = os.path.join(PATH_BASE, 'bin')

SCRIPTS = None
if os.path.exists(PATH_BIN):
    SCRIPTS = [os.path.join('bin', f) for f in os.listdir(PATH_BIN) if os.path.join(PATH_BIN, f)]

f = open(os.path.join(PATH_BASE, 'README.rst'))
README = f.read()
f.close()

__plugin_name__ = 'WebAPI'
__version__ = '.'.join(map(str, VERSION))
__description__ = 'Plugin for Deluge WebUI providing sane JSON API.'
__long_description__ = __description__
__author__ = 'Igor `idle sign` Starikov'
__author_email__ = 'idlesign@yandex.ru'
__license__ = 'BSD 3-Clause License'
__url__ = 'https://github.com/idlesign/deluge-webapi'


__pkg_data__ = {__plugin_name__.lower(): ['data/*']}

setup(
    name=__plugin_name__,
    version=__version__,
    url=__url__,

    description=__description__,
    long_description=README,
    license=__license__,

    author=__author__,
    author_email=__author_email__,

    packages=['webapi'],
    include_package_data=True,
    zip_safe=False,
    package_data = __pkg_data__,

    install_requires=[],
    scripts=SCRIPTS,

    classifiers=[
        # As in https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: BSD License',
        'Environment :: Plugins',
        'Intended Audience :: End Users/Desktop',
    ],

    entry_points="""
    [deluge.plugin.core]
    %s = %s:CorePlugin
    [deluge.plugin.gtkui]
    %s = %s:GtkUIPlugin
    [deluge.plugin.web]
    %s = %s:WebUIPlugin
    """ % ((__plugin_name__, __plugin_name__.lower())*3)
)
