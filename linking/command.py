"""Provide Command class."""

import sys

import stclocal


class Command:
    """General class for linking commands."""

    def __init__(self):
        self.make_parser()
        self.args = self.get_args()
        self.main()

    def get_args(self):
        """Get arguments from self.parser."""
        self.args = self.parser.parse_args(sys.argv[2:])

    def add_source_subsource_to_parser(self, parser, required=False):
        """Add arguments to parser for specifying source and sub source."""
        group = parser.add_mutually_exclusive_group(required=required)
        group.add_argument(
            '-s', '--source', required=False, type=str, default=None,
            help='Specify Source')
        group.add_argument(
            '-ss', '--subsource', required=False, type=str, default=None,
            help="Specify Sub Source")

    def add_channel_item_linnworks_item_to_parser(self):
        """Add arguments to parser for specifying channel item."""
        channel_group = self.parser.add_mutually_exclusive_group(required=True)
        channel_group.add_argument(
            '-cs', '--channelsku', type=str, help="Channel SKU")
        channel_group.add_argument('-ci', '--id', type=str, help="Channel ID")

        linnworks_group = self.parser.add_mutually_exclusive_group(
            required=True)
        linnworks_group.add_argument(
            '-ls', '--linnsku', type=str, help="Linnworks SKU")
        linnworks_group.add_argument(
            '-i', '--stockid', type=str, help="Linnworks Stock ID (GUID)")

    def get_source_subsource_from_args(self):
        """Set self.source and self.subsource from arguments."""
        source = None
        sub_source = None
        if self.args.source is not None:
            source = stclocal.source_lookup(self.args.source)
        if self.args.subsource is not None:
            sub_source = stclocal.sub_source_lookup(self.args.subsource)
        self.source = source
        self.sub_source = sub_source

    def get_channel_item(
            self, channel_reference_id=None, channel_sku=None,
            sub_source=None):
        """Get channel item from arguments."""
        linking = stclocal.pylinnworks.Linking(sub_source=sub_source)
        if len(linking) != 1:
            raise ValueError
        channel = linking[0]
        for item in channel:
            if item.channel_reference_id == channel_reference_id or \
                    item.sku == channel_sku:
                return item
