import os
import requests
from pathlib import Path
from tqdm import tqdm


def download_files_with_popping(url_file, output_dir):
    """
    Download files from a list of URLs and remove each URL from the file once downloaded.

    Args:
        url_file (str): Path to the file containing URLs (one URL per line).
        output_dir (str): Directory to save downloaded files.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(url_file, "r") as file:
        urls = [line.strip() for line in file if line.strip()]

    total_files = len(urls)
    print(f"Total files to download: {total_files}")

    for idx, url in enumerate(urls, 1):
        file_name = os.path.basename(url)
        output_path = output_dir / file_name

        # Skip if file already exists
        if output_path.exists():
            print(f"[{idx}/{total_files}] File already exists, skipping: {file_name}")
            continue

        print(f"[{idx}/{total_files}] Downloading: {url}")

        try:
            # Download the file with progress bar
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an error for bad HTTP responses
            total_size = int(response.headers.get('content-length', 0))  # Get total file size

            with open(output_path, "wb") as file:
                with tqdm(
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    desc=f"Downloading {file_name}",
                    ncols=80
                ) as progress_bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            progress_bar.update(len(chunk))

            print(f"[{idx}/{total_files}] Download complete: {file_name}")

            # Remove the URL from the file
            remove_downloaded_url(url_file, url)

        except requests.RequestException as e:
            print(f"[{idx}/{total_files}] Failed to download: {url} ({e})")


def remove_downloaded_url(url_file, url_to_remove):
    print(url_to_remove, "is about to remove")
    """
    Remove a specific URL from the URL file.

    Args:
        url_file (str): Path to the URL file.
        url_to_remove (str): The URL to remove from the file.
    """
    with open(url_file, "r") as file:
        urls = file.readlines()

    with open(url_file, "w") as file:
        for url in urls:
            if url.strip() != url_to_remove:
                file.write(url)
    print(url_to_remove, "is removed")


# Specify the path to the URL file and output directory
url_file = "10k_urls.txt"  # Replace with the path to your URL file
output_dir = "../downloads"  # Replace with your target folder

# Call the function
download_files_with_popping(url_file, output_dir)
