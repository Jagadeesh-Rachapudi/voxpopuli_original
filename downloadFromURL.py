# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
from pathlib import Path
import requests
from tqdm import tqdm


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url_file", "-u", type=str, required=True, help="Path to file containing URLs"
    )
    parser.add_argument(
        "--root", "-r", type=str, required=True, help="Path to download directory"
    )
    return parser.parse_args()


def download_url(url, dest_folder, file_name):
    """Custom function to download a file from a URL."""
    dest_folder = Path(dest_folder)
    dest_folder.mkdir(parents=True, exist_ok=True)
    file_path = dest_folder / file_name

    # Skip downloading if file already exists
    if file_path.exists():
        print(f"File already exists, skipping: {file_name}")
        return

    print(f"Downloading: {url}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Downloaded: {file_name}")
    else:
        print(f"Failed to download: {url} (HTTP status code: {response.status_code})")
        raise Exception(f"HTTP status code: {response.status_code}")


def download_from_url_file(url_file, output_dir):
    """
    Download files from a list of URLs in a text file.

    Args:
        url_file (str): Path to the file containing URLs (one URL per line).
        output_dir (str): Directory to save downloaded files.
    """
    with open(url_file, "r") as file:
        urls = file.readlines()

    print(f"Found {len(urls)} URLs to download.")
    for idx, url in enumerate(tqdm(urls, desc="Downloading files"), 1):
        url = url.strip()
        if not url:
            continue
        file_name = Path(url).name  # Get the file name from the URL
        try:
            download_url(url, output_dir, file_name)
        except Exception as e:
            print(f"Error downloading {url}: {e}")


def main():
    args = get_args()
    download_from_url_file(args.url_file, args.root)


if __name__ == '__main__':
    main()
