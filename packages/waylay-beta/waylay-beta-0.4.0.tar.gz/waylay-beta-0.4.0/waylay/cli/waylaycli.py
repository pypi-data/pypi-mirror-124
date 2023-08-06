"""Command line interface for the Waylay Python SDK."""

import argparse
import logging

from waylay import WaylayClient

from .seriescli import init_series_parser, handle_series_cmd


def _init_doc_parser(parser):
    parser.add_argument(
        '-s', '--service', dest='doc_service', nargs='*',
        help='Filter services to document.', default=None
    )
    parser.add_argument(
        '-r', '--resource', dest='doc_resource', nargs='*',
        help='Filter resources to document.', default=None
    )
    parser.add_argument(
        '-l', '--link', dest='doc_link', nargs='*', help='Filter doc sites links.', default=None
    )
    parser.add_argument(
        '-d', '--doc_url', dest='doc_url',
        help='Set the root of the documentation site.', default='https://docs.waylay.io/#'
    )


def _init_srv_parser(parser):
    cmd_parsers = parser.add_subparsers(dest='srv_cmd')
    cmd_parsers.add_parser('list', help='List services.')


CLI_COMMANDS = [CMD_DOC, CMD_SERVICE, CMD_SERIES] = ['doc', 'service', 'series']


def main():
    """Start the waylaycli program."""
    logging.basicConfig()
    parser = argparse.ArgumentParser(
        prog='waylaycli', description='Command line interface to the Waylay Python SDK',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-p', '--profile', dest='profile', nargs='?', help='Configuration profile.', default=None
    )
    parser.add_argument(
        '-l', '--loglevel', dest='log_level', nargs='?',
        default='WARNING', type=lambda _: _.upper(),
        help=f"Log level for waylay packages. One of {','.join(logging._levelToName.values())}.",

    )
    parser.add_argument(
        '--libloglevel', dest='lib_log_level', nargs='?',
        default='WARNING', type=lambda _: _.upper(),
        help=f"Log level for other packages. One of {','.join(logging._levelToName.values())}.",
    )
    cmd_parsers = parser.add_subparsers(dest='cmd')
    _init_doc_parser(cmd_parsers.add_parser(CMD_DOC, help='Generate SDK overview of services.'))
    _init_srv_parser(cmd_parsers.add_parser(CMD_SERVICE, help='Services.'))
    init_series_parser(cmd_parsers.add_parser(CMD_SERIES, help='Interact with waylay timeseries.'))

    args = parser.parse_args()

    def waylay_client():
        return WaylayClient.from_profile(args.profile)

    waylay_logger = logging.getLogger('waylay')
    try:
        import coloredlogs
        coloredlogs.install(level='DEBUG')
    except ImportError:
        pass
    logging.getLogger().setLevel(args.lib_log_level)
    waylay_logger.setLevel(args.log_level)

    if args.cmd == CMD_DOC:
        client = waylay_client()
        client.config.set_local_settings(doc_url=args.doc_url)
        print(client.util.info.action_info_html(
            service=args.doc_service, resource=args.doc_resource, links=args.doc_link
        ))
        return
    if args.cmd == CMD_SERVICE and args.srv_cmd == 'list':
        profile = f'profile "{args.profile}"' if args.profile else 'default profile'
        print(
            f'{"key":^10} '
            f'| {" url for "+profile:^35} '
            f'| description'
        )
        print('-' * 10 + '   ' + '-' * 35 + '   ' + '-' * 30)
        for srv in waylay_client().services:
            print(
                f'{srv.service_key:>10} '
                f'| {srv.root_url:<35} '
                f'| {srv.description}'
            )
        return
    if args.cmd == CMD_SERIES:
        handle_series_cmd(waylay_client(), args)
        return
    parser.print_help()
