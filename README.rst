deluge-webapi
=============
https://github.com/idlesign/deluge-webapi


.. image:: https://img.shields.io/pypi/v/deluge-webapi.svg
    :target: https://pypi.python.org/pypi/deluge-webapi

.. image:: https://landscape.io/github/idlesign/deluge-webapi/master/landscape.svg?style=plastic
   :target: https://landscape.io/github/idlesign/deluge-webapi/master


Description
-----------

*Plugin for Deluge WebUI providing sane JSON API.*

Exposes some sane JSON API through Deluge WebUI (missing out of the box or restyled) so that you can manipulate
Deluge from your programs using HTTP requests.

Supported methods:

* get_torrents
* add_torrent (magnet or file)
* remove_torrent
* get_api_version

Deluge is a lightweight, Free Software, cross-platform BitTorrent client. Download it at http://deluge-torrent.org/

.. note:: Plugin tested on Deluge 1.3.15.


Installation
------------

1. Get plugin egg file, from ``dist/`` (https://github.com/idlesign/deluge-webapi/tree/master/dist) directory.

2. Open Deluge Web UI, go to "Preferences -> Plugins -> Install plugin" and choose egg file.

3. Activate `WebAPI` plugin.


.. note::

    To build .egg file from source code yourself use `python setup.py bdist_egg` command in source code directory.


Documentation
-------------

http://deluge-webapi.readthedocs.org/
