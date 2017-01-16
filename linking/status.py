"""Print current linking status for selling channels.

Passable command for linking CLI used for getting current linking status of
selling channels.

Usage: linking status <args>

Arguments:
    -s    --source        Channel Source
    -ss   --subsource     Channel Sub Source
"""

import argparse
import stclocal

from .command import Command


class Status(Command):
    """Main class of status command."""

    description = 'Get linking status'

    def make_parser(self):
        """Create argument parser and add arguments."""
        self.parser = argparse.ArgumentParser(description='Get Linking Status')
        self.add_source_subsource_to_parser(self.parser)

    def get_args(self):
        """Get arguments from self.parser."""
        super().get_args()
        try:
            self.get_source_subsource_from_args()
        except stclocal.ChannelNotFound:
            return

    def main(self):
        """Print linking status."""
        linking = stclocal.pylinnworks.Linking(
            source=self.source, sub_source=self.sub_source)
        for channel in linking:
            print('{} - {}'.format(channel.source, channel.sub_source))
            print('Total: {}'.format(channel.total))
            print('Unlinked: {}'.format(channel.unlinked))
            print('Linked: {}'.format(channel.linked))
            print()
