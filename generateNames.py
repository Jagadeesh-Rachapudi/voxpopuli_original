import os
from pathlib import Path

def list_downloaded_files(download_directory, output_file):
    """
    List all files in the download directory and save the file names to a text file.

    Args:
        download_directory (str): Path to the directory where files are downloaded.
        output_file (str): Path to the output text file to save file names.
    """
    # Ensure the download directory exists
    download_path = Path(download_directory)
    if not download_path.exists() or not download_path.is_dir():
        print(f"Error: The directory '{download_directory}' does not exist.")
        return

    # List all files in the directory
    downloaded_files = sorted(f.name for f in download_path.glob("*") if f.is_file())

    # Save file names to the output file
    with open(output_file, "w") as file:
        file.write("\n".join(downloaded_files))

    print(f"File names have been saved to '{output_file}'.")

# Define the download directory and output file
download_directory = "../raw_audios"  # Replace with your actual download directory
output_file = "names.txt"

# Call the function
list_downloaded_files(download_directory, output_file)
