import argparse
import sys

from linking.status import Status
from linking.list import List


class LinkingManager:
    commands = {
        'status': Status,
        'list': List}

    def __init__(self):
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
    LinkingManager()

if __name__ == "__main__":
    main()
