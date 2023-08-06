
"""REST client for the Waylay Data Service (broker)."""

from waylay.service import WaylayService

from .series import SeriesResource
from .events import EventsResource


class DataService(WaylayService):
    """REST client for the Waylay Data Service (broker)."""

    config_key = 'data'
    service_key = 'data'
    default_root_url = 'https://data.waylay.io'
    resource_definitions = {
        'series': SeriesResource,
        'events': EventsResource,
    }

    series: SeriesResource
    events: EventsResource
