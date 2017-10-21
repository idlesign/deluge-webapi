Quick Reference
===============

.. note::

    First make sure you're using WebUI and `WebAPI` plugin is active under "Preferences -> Plugins".


Hints
-----

1. WebAPI exists alongside with Deluge built-in JSON API, so all HTTP requests should proceed to

  `http://localhost:8112/json` (or what ever you've got instead of `localhost`)

2. Use POST method for HTTP requests.

3. Make requests with valid JSON (including 'Accept: application/json' and 'Content-Type: application/json' HTTP headers).

4. JSON must include the following fields:

   `id` - message number for identity (could be any)

   `method` - API method name. E.g.: `auth.login`, `webapi.get_torrents`

   `params` - API method parameters (depend on method)

5. Login beforehand.

   * Send {"id": 1, "method": "auth.login", "params": ["your_password_here"]} and receive cookies with auth information.

   * Use those cookies for every request.

6. API answers with an error with the following JSON:

   {"error": "Some error description.", "id": 1, "result": False}

   Check responses for `error` field.

7. Make sure Deluge WebUI is connected to Deluge daemon that makes actual torrent processing.

   * Send {"id": 1, "method": "auth.check_session", "params": []} and verify no error.

8. WebAPI method names start with `webapi.`. (E.g.: `webapi.add_torrent` to call `add_torrent` function).


API Methods
-----------


.. note::

    WebAPI uses torrent hashes to identify torrents, so torrent ID is the same as hash.


**Get torrents info**

`get_torrents(ids=None, params=None)`

Returns information about all or a definite torrent.
Returned information can be filtered by supplying wanted parameter names.

    {"id": 1, "method": "webapi.get_torrents", "params": [["torrent_hash1", "torrent_hash2"], ["name", "comment"]]}


**Add torrent**

`add_torrent(metainfo, options=None)`

Adds a torrent with the given options.
`metainfo` could either be base64 torrent data or a magnet link.

    {"id": 1, "method": "webapi.add_torrent", "params": ["base64_encoded_torrent_file_contents", {"download_location": "/home/idle/downloads/"}]}


**Remove torrent**

`remove_torrent(torrent_id, remove_data=False)`

Removes a given torrent. Optionally can remove data.

    {"id": 1, "method": "webapi.remove_torrent", "params": ["torrent_hash3", True]}


**Get API version**

`get_api_version()`

Returns WebAPI plugin version.

    {"id": 1, "method": "webapi.get_api_version", "params": []}

