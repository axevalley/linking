"""Print current linking status for selling channels.

Passable command for linking CLI used for getting current linking status of
selling channels.

Usage: linking status <args>

Arguments:
    -s    --source        Channel Source
    -ss   --subsource     Channel Sub Source
"""

import argparse
import json
import stclocal

from .command import Command


class Status(Command):
    """Main class of status command."""

    name = 'status'
    description = 'Get linking status'

    def make_parser(self):
        """Create argument parser and add arguments."""
        self.parser = argparse.ArgumentParser(description=self.description)
        self.add_source_subsource_to_parser(self.parser)

    def get_args(self):
        """Get arguments from self.parser."""
        self.args = super().get_args()
        try:
            self.get_source_subsource_from_args()
        except stclocal.ChannelNotFound:
            return

    def main(self):
        """Print linking status."""
        linking = stclocal.pylinnworks.Linking(
            source=self.source, sub_source=self.sub_source)
        data = {'{} - {}'.format(channel.source, channel.sub_source): {
            'Total': channel.total,
            'Linked': channel.linked,
            'Unlinked': channel.unlinked
        } for channel in linking}
        data_string = json.dumps(data, indent=4, separators=(',', ': '))
        self.log(data_string)
        print(data_string)
