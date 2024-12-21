# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import os
from pathlib import Path
from tqdm import tqdm
import requests

from voxpopuli import LANGUAGES, LANGUAGES_V2, YEARS, DOWNLOAD_BASE_URL


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", "-r", type=str, required=True, help="data root path"
    )
    parser.add_argument(
        "--subset", "-s", type=str, required=True,
        choices=["400k", "100k", "10k", "asr"] + LANGUAGES + LANGUAGES_V2,
        help="data subset to download"
    )
    return parser.parse_args()


def download_url(url, dest_folder, file_name):
    """Custom function to download a file from a URL."""
    dest_folder = Path(dest_folder)
    dest_folder.mkdir(parents=True, exist_ok=True)
    file_path = dest_folder / file_name
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
    else:
        raise Exception(f"Failed to download {url}. HTTP status code: {response.status_code}")
    return file_path


def extract_archive(tar_path):
    """Extract a tar archive."""
    # from tarfile import open as tar_open
    # tar_path = Path(tar_path)
    # with tar_open(tar_path, 'r') as tar:
    #     tar.extractall(path=tar_path.parent)


def download(args):
    if args.subset in LANGUAGES_V2:
        languages = [args.subset.split("_")[0]]
        years = YEARS + [f"{y}_2" for y in YEARS]
    elif args.subset in LANGUAGES:
        languages = [args.subset]
        years = YEARS
    else:
        languages = {
            "400k": LANGUAGES,
            "100k": LANGUAGES,
            "10k": LANGUAGES,
            "asr": ["original"]
        }.get(args.subset, None)
        years = {
            "400k": YEARS + [f"{y}_2" for y in YEARS],
            "100k": YEARS,
            "10k": [2019, 2020],
            "asr": YEARS
        }.get(args.subset, None)

    url_list = []
    for l in languages:
        for y in years:
            url_list.append(f"{DOWNLOAD_BASE_URL}/audios/{l}_{y}.tar")

    out_root = Path(args.root) / "raw_audios"
    out_root.mkdir(exist_ok=True, parents=True)
    print(f"{len(url_list)} files to download...")
    for url in tqdm(url_list):
        tar_path = download_url(url, out_root, Path(url).name)
        # extract_archive(tar_path.as_posix())
        # os.remove(tar_path)


def main():
    args = get_args()
    download(args)


if __name__ == '__main__':
    main()
