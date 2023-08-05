import argparse
import sys

from videdit.types import interval


def register_cut_parser(subparsers):
    parser = subparsers.add_parser("cut", help="Create a new video file with only portion(s) that we want to keep")
    parser.add_argument("file", help="Path to the video file that needs to be cut")
    parser.add_argument("intervals", type=interval, nargs="+", help="One or more interval of time to keep in the format 7:10-1:20:30")
    
    output_kind = parser.add_mutually_exclusive_group(required=True)
    output_kind.add_argument("-o", "--output", help="Path where the output file will be generated")
    output_kind.add_argument("-i", "--inplace", action="store_true", help="Overwrite original file with output file")


def create_main_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    register_cut_parser(subparsers)

    return parser


def parse_args():
    parser = create_main_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        print("\n[INFO] No command specified...")
        sys.exit(0)

    return args
