#!/usr/bin/env python


import os
import json
import argparse
from pathlib import Path
from distutils.util import strtobool
from eossr.api.zenodo import ZenodoAPI
from eossr.api.zenodo.http_status import ZenodoHTTPStatus
from eossr.metadata.codemeta2zenodo import parse_codemeta_and_write_zenodo_metadata_file


def create_zenodo_metadata(metadata_filename, repo_root_dir='./'):
    """
    Checks for a zenodo metadata file, otherwise it looks for a codemeta.json file to create a the .zenodo.json file

    param metadata_filename: str
        path and name to the zenodo metada json file
        NOT TO BE CHANGED. The file must be named `.zenodo.json` and be stored in the root directory of the library.
    """
    # root_dir = find_root_directory()
    root_dir = Path(repo_root_dir)

    files_json = [file for file in os.listdir(root_dir) if file.endswith('.json')]
    print(f'JSON files : {files_json}')

    zenodo_metadata_filename = metadata_filename
    codemeta_file = 'codemeta.json'

    if codemeta_file in files_json and zenodo_metadata_filename not in files_json:
        print(f"\nCreating {zenodo_metadata_filename} automatically at the CI pipeline.\n")
        parse_codemeta_and_write_zenodo_metadata_file(codemeta_file, zenodo_metadata_filename)

    elif os.path.isfile(zenodo_metadata_filename):
        print(f"\n{zenodo_metadata_filename} metadata file found in the root directory of the library ! \n")
        pass

    else:
        print(f"\n{codemeta_file} not found, thus any zenodo_metadata file `{zenodo_metadata_filename}` was"
              f" created during the CI pipeline."
              f"Please provide one so that the CI can run correctly (examples in the 'codemeta_utils' directory)")
        exit(-1)


def main():
    parser = argparse.ArgumentParser(description="Upload a new version of an existing deposit to Zenodo")

    parser.add_argument('--token', '-t', type=str,
                        dest='zenodo_token',
                        help='Personal access token to (sandbox)Zenodo',
                        required=True)

    parser.add_argument('--sandbox', '-s', action='store',
                        type=lambda x: bool(strtobool(x)),
                        dest='sandbox_flag',
                        help='Set the Zenodo environment.'
                             'True to use the sandbox, False  (default) to use Zenodo.',
                        default=False)

    parser.add_argument('--input-dir', '-i', type=str,
                        dest='input_directory',
                        help='Path to the directory containing the files to upload.'
                             'ALL files will be uploaded.',
                        required=True)

    parser.add_argument('--record_id', '-id', type=str,
                        dest='record_id',
                        help='record_id of the deposit that is going to be updated by a new version',
                        required=True)

    args = parser.parse_args()

    zenodo = ZenodoAPI(
        access_token=args.zenodo_token,
        sandbox=args.sandbox_flag  # True for sandbox.zenodo.org !! False for zenodo.org
    )

    # 1 - request a new version of an existing deposit
    new_version = zenodo.new_version_entry(args.deposit_id)

    if new_version.status_code < 399:
        print(f" * Status {new_version.status_code}. New version of the {args.deposit_id} entry correctly created !")
    else:
        print(f" ! ERROR; new version of the {args.deposit_id} entry COULD NOT be created.")
        print(new_version.json())

    new_deposition_id = new_version.json()['links']['latest_draft'].rsplit('/')[-1]

    # PRE-2 - If you DO NOT want to erase the old files, comment the following lines
    old_files_ids = [file['id'] for file in new_version.json()['files']]
    for file_id in old_files_ids:
        zenodo.erase_file_entry(
            new_deposition_id,
            file_id
        )

    # 2 - Upload new version of file(s)
    for file in os.listdir(args.input_directory):
        full_path_file = args.input_directory + '/' + file

        new_upload = zenodo.upload_file_entry(
            new_deposition_id,
            name_file=file,
            path_file=full_path_file
        )

        status = ZenodoHTTPStatus(new_upload.status_code, new_upload.json())
        print(f"{status}\n * File {file} correctly uploaded")

    # 3 - Look for a zenodo metadata file, otherwise try to create one
    zenodo_metadata_filename = '.zenodo.json'
    create_zenodo_metadata(zenodo_metadata_filename)

    with open(zenodo_metadata_filename) as json_file:
        update_entry_metadata = json.load(json_file)

    # update_entry_info['metadata']['doi'] = doi  # In the new version of the API the doi is updated automatically.
    update_entry = zenodo.update_metadata_entry(
        new_deposition_id,
        json_metadata=update_entry_metadata
    )

    status = ZenodoHTTPStatus(update_entry['status_code'], update_entry)

    if not status.is_error():
        print(f" * Status {update_entry.status_code}. Repository information correctly uploaded !\n")


    # 4 - publish entry - to publish the entry, uncomment the two lone below
    publish = zenodo.publish_entry(new_deposition_id)

    if publish.status_code == 204:
        print(" * New version of the old deposition correctly published !\n")
        print(f" * Old deposition id {args.deposit_id}, new deposition id {new_deposition_id}")
        print(f" * The new doi should look like 10.5281/{new_deposition_id}. However please")
        print(f" ** Check the upload at {zenodo.zenodo_api_url[:-4]}/deposit/{new_deposition_id}  **")
    else:
        print(f" ! New deposit NOT correctly published ! Status {publish.status_code}\n",
              publish.json())


if __name__ == '__main__':
    main()
