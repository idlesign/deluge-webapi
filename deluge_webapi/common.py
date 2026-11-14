import pkg_resources, os

def get_resource(filename):
    return pkg_resources.resource_filename('webapi', os.path.join('data', filename))
