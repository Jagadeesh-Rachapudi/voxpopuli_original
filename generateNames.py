import os
import time
from pathlib import Path

def monitor_downloads(download_directory, output_file, expected_file_count):
    """
    Monitor a directory for new files and save their names to a text file.

    Args:
        download_directory (str): Path to the directory where files are downloaded.
        output_file (str): Path to the output text file to save file names.
        expected_file_count (int): The total number of expected files.
    """
    # Ensure the download directory exists
    download_path = Path(download_directory)
    if not download_path.exists() or not download_path.is_dir():
        print(f"Error: The directory '{download_directory}' does not exist.")
        return

    # Set to keep track of observed file names
    observed_files = set()

    print(f"Monitoring '{download_directory}' for downloads...")
    while len(observed_files) < expected_file_count:
        # List all files currently in the directory
        current_files = set(f.name for f in download_path.glob("*") if f.is_file())

        # Update observed files
        new_files = current_files - observed_files
        if new_files:
            print(f"New files detected: {', '.join(new_files)}")
            observed_files.update(new_files)

            # Save updated file list to the output file
            with open(output_file, "w") as file:
                file.write("\n".join(sorted(observed_files)))

        # Wait for a short period before checking again
        time.sleep(5)

    print(f"All {expected_file_count} files have been saved to '{output_file}'.")

# Define the download directory, output file, and expected file count
download_directory = "../raw_audios"  # Replace with your actual download directory
output_file = "names.txt"
expected_file_count = 46  # Set the number of files expected

# Call the function
monitor_downloads(download_directory, output_file, expected_file_count)
