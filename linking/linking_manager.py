"""Main class of linking CLI."""

import argparse
import sys

from linking.status import Status
from linking.list import List
from linking.refresh import Refresh
from linking.link import Link
from linking.copylink import CopyLink
from linking.skulink import SKULink


class LinkingManager:
    """Main class of linking CLI.

    Takes commands and calls the relevant command method.
    Usage: linking <command> <args>
    """

    commands = {
        'status': Status,
        'list': List,
        'refresh': Refresh,
        'link': Link,
        'copylink': CopyLink,
        'skulink': SKULink}

    def __init__(self):
        """Parse command line arguments and instanciate command class."""
        command_usage = ['{}\t{}'.format(
                name, com.description) for name, com in self.commands.items()]
        usage = '\n'.join(
            ['linking <command> [<args>]', ''] + command_usage)
        parser = argparse.ArgumentParser(
            description='CLI Interface for managing Linnworks Linking',
            usage=usage)
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])

        if args.command not in self.commands:
            print('Unrecognised command')
            parser.print_help()
            exit(1)
        self.commands[args.command]()


def main():
    """Main method of package."""
    LinkingManager()

if __name__ == "__main__":
    main()
