from importlib.resources import files

from packaging import version

from deluge.common import get_version

DEFAULT_PREFS = {
    "enable_cors": False,
    "allowed_origin": [],
}

# twisted uses byte strings in deluge version 2.1.0 onward
use_bytes = version.parse(get_version()) >= version.parse("2.1.0")


def get_resource(filename):
    return str(files("deluge_webapi").joinpath("data", filename))
