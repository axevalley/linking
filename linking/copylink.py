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

    def copylink(self, source_channel=None, destination_channel=None):
        """Copy linking information from one channel to another."""
        source = stclocal.pylinnworks.Linking(sub_source=source_channel)[0]
        print('Downloading items for {}'.format(str(source)))
        source_items = source.get_all(unlinked=False)
        linking_lookup = {
            item.sku: item.linked_item_id for item in source_items}
        destination = stclocal.pylinnworks.Linking(
            sub_source=destination_channel)[0]
        print('Downloading items for {}'.format(str(destination)))
        destination_items = destination.get_all(linked=False)
        for item in destination_items:
            if item.sku in linking_lookup:
                self.log('{} item {} linked to {} item {}'.format(
                    str(source), str(item.sku), str(destination),
                    str(item.sku)))
                item.link(linking_lookup[item.sku])
