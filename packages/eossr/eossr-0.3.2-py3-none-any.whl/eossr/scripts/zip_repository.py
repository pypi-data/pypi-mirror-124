#!/usr/bin/env python

import argparse
from eossr.utils import zip_repository


def main():
    parser = argparse.ArgumentParser(
        description="Zip the content of a directory (a git project is expected)."
                                     )

    parser.add_argument('--directory', '-d', type=str,
                        dest='directory',
                        help='Path to the directory to be zipped.',
                        required=True)

    parser.add_argument('--name_zip', '-n', type=str,
                        dest='name_zip',
                        help='Zip filename. DEFAULT: directory (basename)',
                        default=None
                        )

    args = parser.parse_args()
    zip_repository(args.directory,
                   args.name_zip,
                   )


if __name__ == '__main__':
    main()
