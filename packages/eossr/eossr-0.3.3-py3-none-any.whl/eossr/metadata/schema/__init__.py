import json
import pkg_resources

__all__ = [
    'codemeta',
    'zenodo'
]


def codemeta():
    return json.load(pkg_resources.resource_stream(__name__, 'codemeta.json'))


def zenodo():
    return json.load(pkg_resources.resource_stream(__name__, '.zenodo.json'))