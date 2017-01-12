import argparse
import stclocal

from .command import Command


class List(Command):

    description = 'Get list of available channels'

    def make_parser(self):
        self.parser = argparse.ArgumentParser(description='List Channels')
        self.add_source_subsource_to_parser()

    def get_args(self):
        super().get_args()
        try:
            self.get_source_subsource_from_args()
        except stclocal.ChannelNotFound:
            return

    def main(self):
        linking = stclocal.pylinnworks.Linking(
            source=self.source, sub_source=self.sub_source)
        for channel in linking:
            print('{}: {} - {}'.format(
                channel.channel_id, channel.source, channel.sub_source))
