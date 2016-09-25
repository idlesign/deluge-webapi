deluge-webapi
=============
https://github.com/idlesign/deluge-webapi


.. image:: https://img.shields.io/pypi/v/deluge-webapi.svg
    :target: https://pypi.python.org/pypi/deluge-webapi

.. image:: https://img.shields.io/pypi/dm/deluge-webapi.svg
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


Installation
------------

1. Get plugin egg file, e.g. `deluge_webapi-0.1.0-py2.7.egg`.

2. **IMORTANT**: rename it - strip `deluge_` from its name, e.g. `webapi-0.1.0-py2.7.egg`.

3. Open Deluge Web UI, go to "Preferences -> Plugins -> Install plugin" and choose `webapi-0.1.0-py2.7.egg` file.

4. Activate `webapi` plugin.


.. note::

    To build .egg file from source code yourself use `python setup.py bdist_egg` command in source code directory.


Documentation
-------------

http://deluge-webapi.readthedocs.org/
