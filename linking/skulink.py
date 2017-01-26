"""Link channel items to Linnworks items where SKUs match.

Passable command for linking CLI used for linking items with matching SKUs.

Usage: linking copylink <args>

Arguments:
    -ss --subsource     Sub Source to be linked
"""

import argparse
import stclocal

from . command import Command


class SKULink(Command):
    """Main class of skulink command."""

    name = 'skulink'
    description = """Link channel items to Linnworks items with matchin
        SKUS."""

    def make_parser(self):
        """Create argument parser and add arguments."""
        self.parser = argparse.ArgumentParser(description=self.description)
        self.parser.add_argument(
            'channels', nargs='?', default=None, type=str)

    def get_args(self):
        """Get arguments from self.parser."""
        self.args = super().get_args()
        if self.args.channels is None:
            source = None
            sub_source = None
        else:
            try:
                source = stclocal.source_lookup(self.args.channels)
            except stclocal.ChannelNotFound:
                try:
                    sub_source = stclocal.sub_source_lookup(self.args.channels)
                except:
                    print('Channel not found')
                    exit(1)
                source = None
            else:
                sub_source = None
        self.channels = stclocal.pylinnworks.Linking(
            sub_source=sub_source, source=source)

    def main(self):
        """Link items by SKU."""
        self.linked_count = 0
        self.not_linked_count = 0
        for channel in self.channels:
            self.skulink_channel(channel)
        print('{} items linked.'.format(self.linked_count))
        print('{} items failed to link.'.format(self.not_linked_count))

    def skulink_channel(self, channel):
        """Link channel by SKU."""
        items = channel.get_items(linked=False)
        for item in items:
            self.skulink_item(item)

    def skulink_item(self, item):
        """Link item by SKU."""
        try:
            linn_item = stclocal.pylinnworks.Inventory.get_item_by_SKU(
                item.sku)
        except:
            self.not_linked_count += 1
            return
        else:
            self.log('{} {} item {} linked to {}: {}'.format(
                item.source, item.sub_source, item.sku, linn_item.sku,
                linn_item.stock_id))
            item.link(linn_item.stock_id)
            self.linked_count += 1
