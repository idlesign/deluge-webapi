deluge-webapi
=============
https://github.com/idlesign/deluge-webapi


.. image:: https://pypip.in/d/deluge-webapi/badge.png
        :target: https://crate.io/packages/deluge-webapi


Description
-----------

*Plugin for Deluge WebUI providing sane JSON API.*

Exposes some sane JSON API through Deluge WebUI (missing out of the box or restyled) so that you can manipulate
Deluge from your programs using HTTP requests.

Deluge is a lightweight, Free Software, cross-platform BitTorrent client. Download it at http://deluge-torrent.org/


Installation
------------

* Get plugin egg file, e.g. `deluge_webapi-0.1.0-py2.7.egg`.

* **IMORTANT**: rename it - strip `deluge_` from its name, e.g. `webapi-0.1.0-py2.7.egg`.

* Open Deluge Web UI, go to "Preferences -> Plugins -> Install plugin" and choose `webapi-0.1.0-py2.7.egg` file.

* Activate `webapi` plugin.

.. note::

    To build .egg file from source code yourself use `python setup.py bdist_egg` command in source code directory.


Documentation
-------------

http://deluge-webapi.readthedocs.org/
