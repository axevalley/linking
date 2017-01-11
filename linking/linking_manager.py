import argparse
import sys

import stclocal


class LinkingManager:

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='CLI Interface for managing Linnworks Linking',
            usage='''linking <command> [<args>]

            status  Gets current status of linking
            list    Gets list of available channels
            ''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print('Unrecognised command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def status(self):
        parser = argparse.ArgumentParser(description='Get Linking Status')
        self.add_source_subsource_to_parser(parser)
        args = parser.parse_args(sys.argv[2:])
        try:
            source, sub_source = self.get_source_subsource_from_args(args)
        except stclocal.ChannelNotFound:
            return
        self.print_status(source, sub_source)

    def add_source_subsource_to_parser(self, parser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '-s', '--source', required=False, type=str, default=None,
            help='Specify Source')
        group.add_argument(
            '-ss', '--subsource', required=False, type=str, default=None,
            help="Specify Sub Source")

    def list(self):
        parser = argparse.ArgumentParser(description='List Channels')
        self.add_source_subsource_to_parser(parser)
        args = parser.parse_args(sys.argv[2:])
        try:
            source, sub_source = self.get_source_subsource_from_args(args)
        except stclocal.ChannelNotFound:
            return
        linking = stclocal.pylinnworks.Linking(
            source=source, sub_source=sub_source)
        for channel in linking:
            print('{}: {} - {}'.format(
                channel.channel_id, channel.source, channel.sub_source))

    def get_source_subsource_from_args(self, args):
        source = None
        sub_source = None
        if args.source is not None:
            source = stclocal.source_lookup(args.source)
        if args.subsource is not None:
            sub_source = stclocal.sub_source_lookup(args.subsource)
        return source, sub_source

    def print_status(self, source, sub_source):
        linking = stclocal.pylinnworks.Linking(
            source=source, sub_source=sub_source)
        for channel in linking:
            print('{} - {}'.format(channel.source, channel.sub_source))
            print('Total: {}'.format(channel.total))
            print('Unlinked: {}'.format(channel.unlinked))
            print('Linked: {}'.format(channel.linked))
            print()


def main():
    LinkingManager()

if __name__ == "__main__":
    main()
