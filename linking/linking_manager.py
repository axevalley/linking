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

    def add_source_subsource_to_parser(self, parser, required=False):
        group = parser.add_mutually_exclusive_group(required=required)
        group.add_argument(
            '-s', '--source', required=False, type=str, default=None,
            help='Specify Source')
        group.add_argument(
            '-ss', '--subsource', required=False, type=str, default=None,
            help="Specify Sub Source")

    def add_channel_item_linnworks_item_to_parser(self, parser):
        channel_group = parser.add_mutually_exclusive_group(required=True)
        channel_group.add_argument(
            '-cs', '--sku', type=str, help="Channel SKU")
        channel_group.add_argument('-ci', '--id', type=str, help="Channel ID")

        linnworks_group = parser.add_mutually_exclusive_group(required=True)
        linnworks_group.add_argument(
            '-ls', '--linnsku', type=str, help="Linnworks SKU")
        linnworks_group.add_argument(
            '-i', '--stockid', type=str, help="Linnworks Stock ID (GUID)")

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

    def link(self):
        parser = argparse.ArgumentParser(
            description="Link Linnworks Item and Channel Item")
        parser.add_argument(
            '-c', '--channel', required=True, type=str, default=None,
            help="Specify Channel")
        self.add_channel_item_linnworks_item_to_parser(parser)
        args = parser.parse_args(sys.argv[2:])
        if args.stockid is not None:
            stock_id = args.stock_id
        else:
            stock_id = stclocal.PyLinnworks.Inventory.get_stock_id_by_SKU(
                args.sku)
        channel_item = self.get_channel_item(
            channel_reference_id=args.id, channel_sku=args.sku,
            channel=args.channel)
        channel_item.link(stock_id)

    def get_channel_item(
            self, channel_reference_id=None, channel_sku=None,
            sub_source=None):
        linking = stclocal.pylinnworks.Linking(sub_source=sub_source)
        if len(linking) != 1:
            raise ValueError
        channel = linking[0]
        for item in channel:
            if item.channel_reference_id == channel_reference_id or \
                    item.sku == channel_sku:
                return item

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
