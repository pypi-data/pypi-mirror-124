"""REST definitions for the 'series' entity of the 'data' service."""

from waylay.service import WaylayResource
from waylay.service import decorators

DEFAULT_DECORATORS = [decorators.exception_decorator, decorators.return_body_decorator]


class EventsResource(WaylayResource):
    """REST Resource for the 'events' ingestion of the 'data' service."""

    link_roots = {
        'doc': '${doc_url}/api/broker/?id='
    }

    actions = {
        'post': {
            'method': 'POST', 'url': '/resources/{}/events',
            'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator([]),
            ],
            'description': (
                'Forward a json message to the rule engine, '
                'time series database and/or document store for a given resource.'
            ),
            'links': {
                'doc': 'posting-data-to-the-storage-and-rule-engine'
            },
        },
        'bulk': {
            'method': 'POST', 'url': '/messages',
            'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator([])
            ],
            'description': (
                'Forward an array of json messages to the rule engine, '
                'time series database and/or document store.'
            ),
            'links': {
                'doc': 'posting-array-of-data'
            },
        },
        'remove': {
            'method': 'DELETE', 'url': '/resources/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Remove all data for a resource.',
            'links': {
                'doc': 'all-data-for-a-resource'
            },
        },
    }
