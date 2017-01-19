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
        self.parser.add_argument('-s', '--subsource', required=True, type=str)

    def get_args(self):
        """Get arguments from self.parser."""
        self.args = super().get_args()
        try:
            self.sub_source = stclocal.sub_source_lookup(self.args.subsource)
        except:
            print('Channel not found')
            exit(1)

    def main(self):
        """Link items by SKU."""
        channel = stclocal.pylinnworks.Linking.get_channel_by_sub_source(
            sub_source=self.sub_source)
        items = channel.get_items(linked=False)
        for item in items:
            try:
                linn_item = stclocal.pylinnworks.Inventory.get_item_by_SKU(
                    item.sku)
            except:
                continue
            else:
                self.log('{} {} item {} linked to {}: {}'.format(
                    item.source, item.sub_source, item.sku, linn_item.sku,
                    linn_item.stock_id))
                item.link(linn_item.stock_id)
