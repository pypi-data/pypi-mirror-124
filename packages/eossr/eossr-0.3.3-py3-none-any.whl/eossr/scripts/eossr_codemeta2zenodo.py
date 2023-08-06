#!/usr/bin/env python

import sys
import argparse
from pathlib import Path
from distutils.util import strtobool
from eossr.metadata.codemeta2zenodo import parse_codemeta_and_write_zenodo_metadata_file


def query_yes_no(question, default="yes"):
    """
    Ask a yes/no question via raw_input() and return their answer.

    :param question: str
        question to the user
    :param default: str - "yes", "no" or None
        resumed answer if the user just hits <Enter>.
        "yes" or "no" will set a default answer for the user
        None will require a clear answer from the user

    :return: bool - True for "yes", False for "no"
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        else:
            try:
                return bool(strtobool(choice))
            except:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")


def query_continue(question, default="no"):
    """
    Ask a question and if the answer is no, exit the program.
    Calls `query_yes_no`.

    :param question: str
    :param default: str

    :return answer: bool - answer from query_yes_no
    """
    answer = query_yes_no(question, default=default)
    if not answer:
        sys.exit("Program stopped by user")
    else:
        return answer


def main():
    parser = argparse.ArgumentParser(
        description="Converts a metadata descriptive files from the the CodeMeta to the Zenodo schema. "
                    "Creates a .zenodo.json file from a codemeta.json file."
        )

    parser.add_argument(
        '--input_codemeta_file', '-i', type=str,
        dest='codemeta_file',
        help='Path to a codemeta.json file',
        required=True
    )

    args = parser.parse_args()

    codemeta_file = Path(args.codemeta_file)

    # Check if file exists and it is named as it should
    if not codemeta_file.exists():
        print("\n\tThe input file doest not exists. Exiting.")
        sys.exit(-1)

    if not codemeta_file.name.startswith('codemeta') or not \
            codemeta_file.name.endswith('.json'):
        print(f"\n\t{codemeta_file.name} either does not starts with the `codemeta` prefix or "
              f"either it does not finishes with a `.json` suffix. Exiting")
        sys.exit(-1)

    directory_codemeta = codemeta_file.parent.absolute()
    zenodo_metadata_file = directory_codemeta / '.zenodo.json'

    # Check overwrite zenodo file if exists
    if zenodo_metadata_file.exists():
        cont = query_continue(
            f"\nThe {zenodo_metadata_file.name} file already exists."
            f"\nIf you continue you will overwrite the file with the metadata found in the {codemeta_file.name} file. "
            f"\n\nAre you sure ?")

    # Parse the codemeta.json file and create the .zenodo.json file
    parse_codemeta_and_write_zenodo_metadata_file(
        codemeta_file,
        outdir=directory_codemeta
    )
    print("\nConversion codemeta2zenodo done.\n")


if __name__ == "__main__":
    main()
