#!/usr/bin/env python
# This script is meant to be used by the continuous integration of a git repository to upload its content to the OSSR


import shutil
import argparse
import json
from pathlib import Path
from distutils.util import strtobool
from copy import deepcopy
from eossr.api.zenodo import ZenodoAPI, Record, SimilarRecordError
from eossr.metadata.codemeta2zenodo import converter
from eossr.utils import zip_repository


def upload(zenodo_token, sandbox_flag, upload_directory, record_id=None, zip_root_dir=False, erase_previous_files=True,
           force_new_record=False, publish=True):
    """
    Prepares the upload of the content of `upload_directory` to the OSSR.
    There must be a metadata file present in the directory to be uploaded.

    It first searches for similar record uploaded by the same Zenodo user.
    The codemeta.json file will be copied to the `upload_directory`.
    Uploads the content of `upload_directory` using the ZenodoAPI.

    :param zenodo_token: str
        Personal access token to the (sandbox.)zenodo.org/api
    :param sandbox_flag: bold
        Set the Zenodo environment. True to use the sandbox, False to use Zenodo.
    :param upload_directory: str or Path
        Path to the directory whose content will be uploaded to the OSSR.
    :param record_id: int or str
        Zenodo record-id of the record that is going to be updated.
        If no record_id is provided, a new record will be created in the OSSR.
    :param zip_root_dir: bool
        If True, the content of the root dir of the repository will be zipped and moved to the `upload_directory` to
        be uploaded to the OSSR.
    :param erase_previous_files: bool
        If True (default), it will erase the files of previous versions of the record before creating and updating the
        new version of the record. If False, it will not erase any file and old files will be included in the
        new version.
    :param force_new_record: bool
        If False (default), a new version of the `record_id` record will be created.
        If True, a new record - despite that it might already exists one - will be created.
    :param publish: bool
        If true, publish the record. Otherwise, the record is prepared but publication must be done manually. This
        is useful to check or discard the record before publication.

    :return: The `record_id` of the record created/uploaded
        `ZenodoAPI.upload_dir_content` answer
    """

    zenodo = ZenodoAPI(access_token=zenodo_token, sandbox=sandbox_flag, proj_root_dir=upload_directory)

    # Loads the metadata files if exists
    if zenodo.path_zenodo_file.exists():
        print(f"Record metadata based on zenodo file {zenodo.path_zenodo_file}")
        with open(zenodo.path_zenodo_file) as file:
            metadata = json.load(file)
    elif zenodo.path_codemeta_file.exists():
        print(f"Record metadata based on codemeta file {zenodo.path_codemeta_file}")
        with open(zenodo.path_codemeta_file) as file:
            codemeta = json.load(file)
        metadata = converter(codemeta)
    else:
        raise FileNotFoundError("No metadata provided")

    metadata_for_check = {'metadata': deepcopy(metadata)}
    metadata_for_check['id'] = 1  # fake id to create fake record
    metadata_for_check['metadata']['doi'] = 1  # fake doi to create fake record
    record = Record(metadata_for_check)

    ## Searches for similar records
    similar_records = zenodo.find_similar_records(record)
    if similar_records and not force_new_record and not record_id:
        raise SimilarRecordError(
            f"There are similar records in your own records: {similar_records}."
            "If you want to update an existing record, provide its record id to make a new version."
            "If you still want to make a new record, use --force-new-record.")

    # Zips the root directory content and moves the file to the `input dir` for a later upload
    if zip_root_dir:
        repo_zipped = zip_repository(zenodo.root_dir, zip_filename=f'{zenodo.root_dir.name}')
        shutil.move(repo_zipped, upload_directory)

    # If a codemeta.json file exists and is not present in the upload dir, copy it into this dir.
    if not Path(upload_directory).joinpath('codemeta.json').exists() and \
            zenodo.path_codemeta_file.exists():
        shutil.copy(zenodo.path_codemeta_file, upload_directory)

    return zenodo.upload_dir_content(upload_directory,
                                     record_id=record_id,
                                     metadata=metadata,
                                     erase_previous_files=erase_previous_files,
                                     publish=publish
                                     )


def main():
    parser = argparse.ArgumentParser(description="Upload a directory to the OSSR as record."
                                                 "The directory must include a valid zenodo or codemeta file to be used"
                                                 "as metadata source for the upload."
                                                 "If not record_id is passed, a new record is created."
                                                 "Otherwise, a new version of the existing record is created."
                                     )

    parser.add_argument('--token', '-t', type=str,
                        dest='zenodo_token',
                        help='Personal access token to (sandbox)Zenodo',
                        required=True)

    parser.add_argument('--sandbox', '-s', action='store',
                        type=lambda x: bool(strtobool(x)),
                        dest='sandbox_flag',
                        help='Set the Zenodo environment.'
                             'True to use the sandbox, False (default) to use Zenodo.',
                        default=False)

    parser.add_argument('--input-dir', '-i', type=str,
                        dest='input_directory',
                        help='Path to the directory containing the files to upload.'
                             'All files will be uploaded.',
                        required=True)

    parser.add_argument('--record_id', '-id', type=str,
                        dest='record_id',
                        help='record_id of the deposit that is going to be updated by a new version',
                        default=None,
                        required=False)

    parser.add_argument('--force-new-record',
                        action='store_true',
                        dest='force_new_record',
                        help='Force the upload of a new record in case a similar record is found '
                             'in the user existing ones',
                        )

    parser.add_argument('--no-publish',
                        action='store_false',
                        dest='publish',
                        help='Optional tag to specify if the record will NOT be published. '
                             'Useful for checking the record before publication of for CI purposes.',
                        )

    args = parser.parse_args()

    new_record_id = upload(args.zenodo_token,
                           args.sandbox_flag,
                           args.input_directory,
                           record_id=args.record_id,
                           force_new_record=args.force_new_record,
                           publish=args.publish)

    return new_record_id


if __name__ == '__main__':
    main()
