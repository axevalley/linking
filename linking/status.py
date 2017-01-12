import argparse
import stclocal

from .command import Command


class Status(Command):

    description = 'Get linking status'

    def make_parser(self):
        self.parser = argparse.ArgumentParser(description='Get Linking Status')
        self.add_source_subsource_to_parser(self.parser)

    def get_args(self):
        super().get_args()
        try:
            self.get_source_subsource_from_args()
        except stclocal.ChannelNotFound:
            return

    def main(self):
        self.print_status(self.source, self.sub_source)

    def print_status(self, source, sub_source):
        linking = stclocal.pylinnworks.Linking(
            source=source, sub_source=sub_source)
        for channel in linking:
            print('{} - {}'.format(channel.source, channel.sub_source))
            print('Total: {}'.format(channel.total))
            print('Unlinked: {}'.format(channel.unlinked))
            print('Linked: {}'.format(channel.linked))
            print()
