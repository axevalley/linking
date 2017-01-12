import argparse
import stclocal
from . command import Command


class Link(Command):

    description = 'Link Linnworks item to channel item'

    def make_parser(self):
        self.parser = argparse.ArgumentParser(
            description="Link Linnworks Item and Channel Item")
        self.parser.add_argument(
            '-c', '--channel', required=True, type=str, default=None,
            help="Specify Channel")
        self.add_channel_item_linnworks_item_to_parser()

    def get_args(self):
        super().get_args()
        if self.args.stockid is not None:
            self.stock_id = self.args.stock_id
        else:
            self.stock_id = stclocal.PyLinnworks.Inventory.get_stock_id_by_SKU(
                self.args.sku)

    def main(self):
        channel_item = self.get_channel_item(
            channel_reference_id=self.args.id, channel_sku=self.args.sku,
            channel=self.args.channel)
        channel_item.link(self.stock_id)
