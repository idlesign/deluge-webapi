deluge-webapi documentation
===========================
https://github.com/idlesign/deluge-webapi



Description
-----------

*Plugin for Deluge WebUI providing sane JSON API.*

Exposes some sane JSON API through Deluge WebUI (missing out of the box or restyled) so that you can manipulate
Deluge from your programs using HTTP requests.


Requirements
------------

1. Python 2.7+
2. Deluge 1.3.15+


Installation
------------

    * Get plugin egg file, from ``dist/`` (https://github.com/idlesign/deluge-webapi/tree/master/dist) directory.

    * Open Deluge Web UI, go to "Preferences -> Plugins -> Install plugin" and choose egg file.

        .. note::

            To build .egg file from source code yourself use `python setup.py bdist_egg` command in source code directory.

    * Activate `WebAPI` plugin.

    * You're ready.


Table of Contents
-----------------

.. toctree::
    :maxdepth: 2

    quickstart


Get involved into deluge-webapi
-------------------------------

**Submit issues.** If you spotted something weird in application behavior or want to propose a feature you can do that at https://github.com/idlesign/deluge-webapi/issues

**Write code.** If you are eager to participate in application development, fork it at https://github.com/idlesign/deluge-webapi, write your code, whether it should be a bugfix or a feature implementation, and make a pull request right from the forked project page.

**Spread the word.** If you have some tips and tricks or any other words in mind that you think might be of interest for the others — publish it.


More things
-----------

* You might be interested in considering other Deluge plugins at http://dev.deluge-torrent.org/wiki/Plugins/
* Or you might be interested in a PHP Deluge API wrapper: https://github.com/kaysond/deluge-php

