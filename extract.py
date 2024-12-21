import os
import tarfile
from pathlib import Path

def extract_and_organize(download_dir, target_dir):
    """
    Extract `.tar` files from the download directory into organized folders.

    Args:
        download_dir (str): Path to the directory containing `.tar` files.
        target_dir (str): Path to the directory where files will be extracted.
    """
    download_path = Path(download_dir)
    target_path = Path(target_dir)

    # Ensure target directory exists
    target_path.mkdir(parents=True, exist_ok=True)

    # List all `.tar` files in the download directory
    tar_files = [f for f in download_path.glob("*.tar") if f.is_file()]

    if not tar_files:
        print("No .tar files found in the downloads directory.")
        return

    print(f"Found {len(tar_files)} .tar files to extract.")

    for tar_file in tar_files:
        file_name = tar_file.stem  # Get the file name without extension (e.g., "en_2019")
        try:
            # Split into language and year based on underscore
            lang, year = file_name.split("_")
        except ValueError:
            print(f"Skipping invalid file name format: {tar_file.name}")
            continue

        # Define extraction folder: target_dir/lang/year
        extract_folder = target_path / lang / year
        extract_folder.mkdir(parents=True, exist_ok=True)

        print(f"Extracting {tar_file.name} to {extract_folder}...")

        try:
            # Extract the tar file and flatten the structure
            with tarfile.open(tar_file, "r") as tar:
                for member in tar.getmembers():
                    # Ensure files are extracted directly into the target directory
                    member_path = Path(member.name)
                    member.name = member_path.name  # Keep only the file name
                    tar.extract(member, path=extract_folder)
            print(f"Extraction complete: {tar_file.name}")
        except tarfile.TarError as e:
            print(f"Failed to extract {tar_file.name}: {e}")

    print("All files processed. Original .tar files are retained.")

# Define paths
download_dir = "../downloads"  # Directory containing .tar files
target_dir = "../raw_audios"   # Directory where extracted files will be organized

# Call the function
extract_and_organize(download_dir, target_dir)
