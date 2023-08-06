import json
import requests
import shutil
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path

__all__ = [
    'ZipUrl',
    'get_codemeta_from_zipurl',
    'zip_repository',
]


class ZipUrl:

    def __init__(self, url):
        self.url = url
        self.content = requests.get(self.url)

    @property
    def filelist(self):
        with ZipFile(BytesIO(self.content.content)) as zipobj:
            return zipobj.namelist()

    def find_files(self, filename):
        """
        return the path of files in the archive matching `filename`

        :param filename: string
        :return: list[str]
        """
        matching_files = [f for f in self.filelist if Path(f).name == filename]
        if len(matching_files) == 0:
            raise FileNotFoundError(f"No file named {filename} in {self.url}")
        else:
            return matching_files

    def extract_file(self, filepath):
        with ZipFile(BytesIO(self.content.content)) as zipobj:
            return zipobj.extract(filepath)


def get_codemeta_from_zipurl(url):
    """
    Extract and reads codemeta metadata from a zip url.
    A codemeta.json file must be present in the zip archive.

    :param url: string
        url to a zip file
    :return: dictionnary
        metadata in the codemeta.json file in the zip archive
    """
    zipurl = ZipUrl(url)
    codemeta_paths = zipurl.find_files('codemeta.json')
    # if there are more than one codemeta file in the archive, we consider the one in the root directory, hence the
    # one with the shortest path
    codemeta_path = min(codemeta_paths, key=len)
    with open(zipurl.extract_file(codemeta_path)) as file:
        codemeta = json.load(file)

    return codemeta


def zip_repository(directory, zip_filename=None):
    """
    Zip the content of `directory` into `./zip_filename.zip`.
    If a .git directory exists within `directory`, it will erase it before zipping the repository

    :param directory: str or Path
        Path to the directory to be zipped
    :param zip_filename: str
        Zip filename name, used to name the zip file. If None, the zip will be named as the directory provided.

    :return: zip_filename: path to the zip archive
    """
    # prepare zip archive
    directory = Path(directory)
    zip_filename = f'{directory.absolute().name}' if zip_filename is None \
        else f'{zip_filename.replace(".zip", "")}'
    print(f" * Zipping the content of {directory.name} into {zip_filename}.zip")

    # Copy the content of `directory` to `tmp_dir/directory`
    tmp_dir = Path('../tmp_dir/')
    shutil.copytree(directory, tmp_dir.joinpath(directory.name))

    # If a `.git` directory exists, erase it in the copy of the directory
    if tmp_dir.joinpath(directory.name, '.git').exists():
        shutil.rmtree(tmp_dir.joinpath(directory.name, '.git'))

    # Zip the content of tmp_dir with base_dir as common prefix for all files
    shutil.make_archive(zip_filename, 'zip', root_dir=tmp_dir, base_dir=directory.name)
    # Zip file is create in current directory
    shutil.rmtree(tmp_dir)

    print(f"Zipping done: {zip_filename}.zip")
    return zip_filename + '.zip'
