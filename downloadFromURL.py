import os
import requests
from pathlib import Path
from tqdm import tqdm
import time


def download_files_with_details(url_file, output_dir):
    """
    Download files from a list of URLs with detailed progress logging.

    Args:
        url_file (str): Path to the file containing URLs (one URL per line).
        output_dir (str): Directory to save downloaded files.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Read URLs from the file
    with open(url_file, "r") as file:
        urls = [line.strip() for line in file if line.strip()]

    total_files = len(urls)
    downloaded_files = 0

    print(f"Total files to download: {total_files}")

    for idx, url in enumerate(urls, 1):
        file_name = os.path.basename(url)
        output_path = Path(output_dir) / file_name

        # Skip if file already exists
        if output_path.exists():
            print(f"[{idx}/{total_files}] File already exists, skipping: {file_name}")
            downloaded_files += 1
            continue

        print(f"[{idx}/{total_files}] Downloading: {url}")

        start_time = time.time()
        try:
            # Start downloading
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an error for bad HTTP responses
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            with open(output_path, "wb") as file:
                with tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    desc=f"Downloading {file_name}",
                    ncols=80
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
                            pbar.update(len(chunk))

            elapsed_time = time.time() - start_time
            speed = downloaded_size / elapsed_time / 1024  # Speed in KB/s
            print(
                f"[{idx}/{total_files}] Download complete: {file_name} "
                f"(Size: {total_size / (1024 * 1024):.2f} MB, Time: {elapsed_time:.2f}s, Speed: {speed:.2f} KB/s)"
            )
            downloaded_files += 1

        except requests.RequestException as e:
            print(f"[{idx}/{total_files}] Failed to download: {url} ({e})")

    remaining_files = total_files - downloaded_files
    print(f"\nSummary:")
    print(f"Total files: {total_files}")
    print(f"Downloaded files: {downloaded_files}")
    print(f"Remaining files: {remaining_files}")
    if remaining_files > 0:
        print(f"Consider rerunning the script to retry failed downloads.")


# Define the path to the URL file and output directory
url_file = "10k_urls.txt"  # Replace with your URL file
output_dir = "../downloads"  # Replace with your target folder

# Call the function
download_files_with_details(url_file, output_dir)
