import stclocal


class LinkingManager:

    def __init__(self):
        self.linking = stclocal.pylinnworks.Linking()

    def status(self):
        for channel in self.linking:
            print('{} - {}'.format(channel.source, channel.sub_source))
            print('Total: {}'.format(channel.total))
            print('Unlinked: {}'.format(channel.unlinked))
            print('Linked: {}'.format(channel.linked))
            print()

    def list(self):
        for channel in self.linking:
            print('{}: {} - {}'.format(
                channel.channel_id, channel.source, channel.sub_source))
