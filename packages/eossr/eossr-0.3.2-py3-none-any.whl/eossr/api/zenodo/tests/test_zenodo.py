#!/usr/bin/env python

import json
import unittest
import requests
import pytest
from pathlib import Path
from os import remove
from os.path import dirname, realpath, join
from eossr.api.zenodo import ZenodoAPI, get_zenodo_records, get_record

ROOT_DIR = dirname(realpath("codemeta.json"))


class TestZenodoApiSandbox(unittest.TestCase):
    def test_initialization_sandbox(self):
        token = 'FakeToken'
        z = ZenodoAPI(access_token=token,
                      sandbox=True,
                      proj_root_dir=ROOT_DIR)

        assert isinstance(z, ZenodoAPI)
        assert z.api_url == 'https://sandbox.zenodo.org/api'
        assert z.access_token == token
        assert type(z.exist_codemeta_file) == bool
        assert type(z.exist_zenodo_metadata_file) == bool
        assert z.root_dir == Path(ROOT_DIR)
        assert z.path_codemeta_file == z.root_dir
        assert z.path_zenodo_metadata_file == z.root_dir
        assert isinstance(z.root_dir, (Path, str))


class TestZenodoAPI(unittest.TestCase):
    def test_initialization(self):
        token = 'FakeToken'
        z = ZenodoAPI(access_token=token,
                      sandbox=False,
                      proj_root_dir=ROOT_DIR)

        assert isinstance(z, ZenodoAPI)
        assert z.api_url == 'https://zenodo.org/api'
        assert z.access_token == token
        assert type(z.exist_codemeta_file) == bool
        assert type(z.exist_zenodo_metadata_file) == bool
        assert z.root_dir == Path(ROOT_DIR)
        assert z.path_codemeta_file == z.root_dir
        assert z.path_zenodo_metadata_file == z.root_dir
        assert isinstance(z.root_dir, (Path, str))

    def test_zenodo_api_methods(self):
        token = 'FakeToken'
        z = ZenodoAPI(access_token=token,
                      sandbox=False,
                      proj_root_dir=ROOT_DIR)

        test_id = '42'
        z.search_codemeta_file()
        test_filename = join(ROOT_DIR, z.path_codemeta_file)
        path_test_filename = '../../tests/'

        fetch_user_entry = z.query_user_entries()
        create_new_entry = z.create_new_entry()
        fetch_single_entry = z.query_entry(
            entry_id=test_id
        )
        # upload_file_entry = z.upload_file_entry(
        #     entry_id=test_id,
        #     name_file=test_filename,
        #     path_file=path_test_filename
        # )
        upload_metadata_entry = z.update_metadata_entry(
            entry_id=test_id,
            json_metadata=test_filename
        )
        erase_entry = z.erase_entry(
            entry_id=test_id
        )
        erase_file_entry = z.erase_file_entry(
            entry_id=test_id,
            file_id=test_id
        )
        publish_entry = z.publish_entry(
            entry_id=test_id
        )
        new_version_entry = z.new_version_entry(
            entry_id=test_id
        )

        community_name = 'escape2020'
        community_entries = z.query_community_records(community_name)
        fetch_ids = z.get_community_records_ids(community_name)
        fetch_filenames = z.get_community_records_titles(community_name)

        assert isinstance(fetch_user_entry, requests.models.Response)
        assert isinstance(create_new_entry, requests.models.Response)
        assert isinstance(fetch_single_entry, requests.models.Response)
        # assert isinstance(upload_file_entry, requests.models.Response)
        assert isinstance(upload_metadata_entry, requests.models.Response)
        assert isinstance(erase_entry, requests.models.Response)
        assert isinstance(erase_file_entry, requests.models.Response)
        assert isinstance(publish_entry, requests.models.Response)
        assert isinstance(new_version_entry, requests.models.Response)
        assert isinstance(community_entries, requests.models.Response)
        assert isinstance(fetch_ids, list)
        assert isinstance(fetch_filenames, list)

    def test_search_codemeta_file(self):
        token = 'FakeToken'
        z = ZenodoAPI(access_token=token,
                      sandbox=False,
                      proj_root_dir=ROOT_DIR)

        assert z.exist_codemeta_file is False
        z.search_codemeta_file()
        assert z.exist_codemeta_file is True

        codemeta_file_path = Path(ROOT_DIR) / 'codemeta.json'
        assert z.path_codemeta_file == codemeta_file_path
        assert codemeta_file_path.is_file()
        print(z.path_codemeta_file, type(z.path_codemeta_file))
        with open(z.path_codemeta_file) as f:
            json.load(f)

    def test_search_zenodo_json_file(self):
        token = 'FakeToken'
        z = ZenodoAPI(access_token=token,
                      sandbox=False,
                      proj_root_dir=ROOT_DIR)

        assert z.exist_zenodo_metadata_file is False
        z.search_zenodo_json_file()
        assert z.exist_zenodo_metadata_file is False

    def test_conversion_codemeta2zenodo_and_search_zenodo_file(self):
        token = 'FakeToken'
        z = ZenodoAPI(access_token=token,
                      sandbox=False,
                      proj_root_dir=ROOT_DIR)

        z.search_codemeta_file()
        z.conversion_codemeta2zenodo()

        z.search_zenodo_json_file()
        assert z.exist_zenodo_metadata_file is True

        zenodo_file_path = Path(ROOT_DIR) / '.zenodo.json'
        assert z.path_zenodo_metadata_file == zenodo_file_path
        assert zenodo_file_path.is_file()
        with open(z.path_zenodo_metadata_file) as f:
            json.load(f)

        remove(z.path_zenodo_metadata_file)


def test_get_zenodo_records():
    l = get_zenodo_records('ESCAPE template project')
    assert len(l) > 1
    all_dois = [r.data['doi'] for r in l]
    assert '10.5281/zenodo.4923992' in all_dois

@pytest.mark.xfail(raises=ValueError)
def test_get_record_42():
    get_record(42)

@pytest.fixture
def test_get_record_4923992():
    record = get_record(4923992)
    assert record.data['conceptdoi'] == '10.5281/zenodo.3572654'
    return record

def test_record(test_get_record_4923992):
    record = test_get_record_4923992
    record.print_info()
    codemeta = record.get_codemeta()
    assert isinstance(codemeta, dict)
    assert codemeta['name'] == 'ESCAPE template project'
    record.get_mybinder_url()

def test_get_record_sandbox():
    record = get_record(520735, sandbox=True)
    assert record.data['doi'] == '10.5072/zenodo.520735'
