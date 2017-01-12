import argparse
import stclocal

from .command import Command


class Refresh(Command):

    description = 'Download up-to-date linking from channel to Linnworks'

    def make_parser(self):
        self.parser = argparse.ArgumentParser(description=self.description)
        self.add_source_subsource_to_parser(self.parser)

    def get_args(self):
        super().get_args()
        try:
            self.get_source_subsource_from_args()
        except stclocal.ChannelNotFound:
            print('Source or Sub Source not found')
            exit(1)

    def main(self):
        linking = stclocal.pylinnworks.Linking(
            source=self.source, sub_source=self.sub_source)
        for channel in linking:
            try:
                channel.download_listings()
            except:
                print("Error updating {}".format(channel))
