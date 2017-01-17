"""Request update of linking information on Linnworks servers.

Passable command for linking CLI used for requesting Linnworks updates it's
current list of items for selling channels.

Usage: linking refresh <args>

Arguments:
    -s    --source        Channel Source
    -ss   --subsource     Channel Sub Source
"""

import argparse
import stclocal

from .command import Command


class Refresh(Command):
    """Main class of request command."""

    description = 'Download up-to-date linking from channel to Linnworks'

    def make_parser(self):
        """Create argument parser and add arguments."""
        self.parser = argparse.ArgumentParser(description=self.description)
        self.add_source_subsource_to_parser(self.parser)

    def get_args(self):
        """Get arguments from self.parser."""
        super().get_args()
        try:
            self.get_source_subsource_from_args()
        except stclocal.ChannelNotFound:
            print('Source or Sub Source not found')
            exit(1)

    def main(self):
        """Send request to update linking information."""
        linking = stclocal.pylinnworks.Linking(
            source=self.source, sub_source=self.sub_source)
        for channel in linking:
            try:
                channel.download_listings()
            except:
                print("Error updating {}".format(channel))
