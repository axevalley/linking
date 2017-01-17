"""List available selling channels.

Passable command for linking CLI used for listing available channels, with
their source and subsource.

Usage: linking refresth <args>

Arguments:
    -s    --source        Channel Source
    -ss   --subsource     Channel Sub Source
"""

import argparse
import stclocal

from .command import Command


class List(Command):
    """Main class of list command."""

    name = 'list'
    description = 'Get list of available channels'

    def make_parser(self):
        """Create argument parser and add arguments."""
        self.parser = argparse.ArgumentParser(description='List Channels')
        self.add_source_subsource_to_parser()

    def get_args(self):
        """Get arguments from self.parser."""
        super().get_args()
        try:
            self.get_source_subsource_from_args()
        except stclocal.ChannelNotFound:
            return

    def main(self):
        """Print channel list."""
        linking = stclocal.pylinnworks.Linking(
            source=self.source, sub_source=self.sub_source)
        for channel in linking:
            print('{}: {} - {}'.format(
                channel.channel_id, channel.source, channel.sub_source))
