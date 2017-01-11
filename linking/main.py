import argparse
from . linking_manager import LinkingManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--status', action='store_true', dest='status')
    parser.add_argument('-l', '--list', action='store_true', dest='list')

    args = parser.parse_args()
    linking_manager = LinkingManager()
    if args.status:
        linking_manager.status()

    if args.list:
        linking_manager.list()
