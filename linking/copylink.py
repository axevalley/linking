"""Use linking information from one channel to link unlinked items on another.

Passable command for linking CLI used for linking items with non-matching
SKUs where the same link is present on another channel.

Usage: linking copylink <args>

Arguments:
    -s  --source        Channel identifier for source channel
    -d --destination    Channel identifier for channel to be linked
"""

import argparse
import stclocal

from . command import Command


class CopyLink(Command):
    """Main class of copylink command."""

    name = 'copylink'
    description = """Link channel according to linking information from
        another channel"""

    def make_parser(self):
        """Create argument parser and add arguments."""
        self.parser = argparse.ArgumentParser(description=self.description)
        self.parser.add_argument(
            '-s', '--source', type=str, required=True,
            help='Identifer for channel to be copied from.')
        self.parser.add_argument(
            '-d', '--destination', type=str, required=True,
            help='Identifer for channel to be linked')

    def get_args(self):
        """Get arguments from self.parser."""
        self.args = super().get_args()
        try:
            self.source_channel = stclocal.sub_source_lookup(self.args.source)
            self.destination_channel = stclocal.sub_source_lookup(
                self.args.destination)
        except stclocal.ChannelNotFound:
            print('Source or Sub Source not found')
            exit(1)

    def main(self):
        """Main method for copylink command."""
        self.copylink(
            source_channel=self.source_channel,
            destination_channel=self.destination_channel)

    def get_channel_item_by_sku(self, channel, sku):
        return channel.get_items(keyword=sku)

    def copylink(self, source_channel=None, destination_channel=None):
        """Copy linking information from one channel to another."""
        source = stclocal.pylinnworks.Linking.get_channel_by_sub_source(
            source_channel)
        destination = stclocal.pylinnworks.Linking.get_channel_by_sub_source(
            destination_channel)
        print('Downloading unlinked items for {}'.format(str(destination)))
        destination_items = destination.get_items(linked=False)
        for item in destination_items:
            try:
                source_item = source.get_item_by_sku(item.sku, unlinked=False)
            except:
                continue
            else:
                self.log('{} {} item {} linked to {} item {}'.format(
                    source_item.source, source_item.sub_source,
                    source_item.sku, str(destination), item.sku))
                item.link(source_item.linked_item_id)
