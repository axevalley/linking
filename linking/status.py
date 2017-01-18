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

    def get_status_string_for_channel(self, channel):
        """Make string from channel status information."""
        channel_name = '{0: <35}'.format(
            '{} {}'.format(channel.source, channel.sub_source))
        total = 'Total: {}'.format(channel.total)
        linked = 'Linked: {}'.format(channel.linked)
        unlinked = 'Unlinked: {}'.format(channel.unlinked)
        return '\t'.join([channel_name, total, linked, unlinked])

    def main(self):
        """Print linking status."""
        linking = stclocal.pylinnworks.Linking(
            source=self.source, sub_source=self.sub_source)
        data = '\n'.join([self.get_status_string_for_channel(
            channel) for channel in linking])
        self.log(data)
        print(data)
