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

    name = 'status'
    description = 'Get linking status'

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
                sub_source = stclocal.sub_source_lookup(self.args.channels)
                source = None
            else:
                sub_source = None
        self.channels = stclocal.pylinnworks.Linking(
            sub_source=sub_source, source=source)

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
        data = '\n'.join([self.get_status_string_for_channel(
            channel) for channel in self.channels])
        self.log(data)
        print(data)
