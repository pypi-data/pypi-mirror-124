"""REST definitions for the 'runtime' entity of the 'byoml' service."""

from .._base import WaylayResource
from .._decorators import (
    return_body_decorator,
    return_path_decorator,
)
from ._decorators import (
    byoml_exception_decorator,
    byoml_retry_decorator,
)


class RuntimeResource(WaylayResource):
    """REST Resource for the 'runtime' entity of the 'byoml' service."""

    link_roots = {
        'doc': '${doc_url}/api/byoml/?id='
    }

    actions = {
        'list': {
            'method': 'GET',
            'url': '/runtimes',
            'decorators': [
                byoml_exception_decorator,
                byoml_retry_decorator,
                return_path_decorator(['runtimes'])
            ],
            'description': 'List runtimes (framework and framework version).',
            'links': {
                'doc': 'runtimes'
            },
        },
        'get': {
            'method': 'GET',
            'url': '/runtimes/{}',
            'decorators': [
                byoml_exception_decorator,
                byoml_retry_decorator,
                return_body_decorator,
            ],
            'description': 'Get a supported runtime.',
            'links': {
                'doc': 'runtimes'
            },
        }
    }
