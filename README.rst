deluge-webapi
=============
https://github.com/idlesign/deluge-webapi


.. image:: https://img.shields.io/pypi/v/deluge-webapi.svg
    :target: https://pypi.python.org/pypi/deluge-webapi


Description
-----------

*Plugin for Deluge WebUI providing sane JSON API.*

Exposes some sane JSON API through Deluge WebUI (missing out of the box or restyled) so that you can manipulate
Deluge from your programs using HTTP requests.

Supported methods:

* ``get_torrents``
* ``add_torrent`` (magnet or file)
* ``remove_torrent``
* ``get_api_version``

Deluge is a lightweight, Free Software, cross-platform BitTorrent client. Download it at http://deluge-torrent.org/

.. note:: Use egg version 0.4.0 or higher for Deluge 2
.. note:: Use egg version 0.3.2 or lower for Deluge 1.x


Installation
------------

1. Get plugin egg file, from ``dist/`` (https://github.com/idlesign/deluge-webapi/tree/master/dist) directory.

2. Open Deluge Web UI, go to "Preferences -> Plugins -> Install plugin" and choose egg file.

3. Activate ``WebAPI`` plugin.

4. In case you use Client-Server setup, you'll need to install the plugin both on client and server, see - https://dev.deluge-torrent.org/wiki/Plugins#Client-ServerSetups


.. note::

    To build .egg file from source code yourself use ``python setup.py bdist_egg`` command in source code directory.


Documentation
-------------

http://deluge-webapi.readthedocs.org/
