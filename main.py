import os
import shutil
import time
import logging
import argparse

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def synchronize_folders(source_folder, replica_folder, interval_seconds, log_file):
    setup_logging(log_file)

    while True:
        # Ensure both folders exist or create them
        if not os.path.exists(source_folder):
            os.makedirs(source_folder)
            logging.info(f"Created source folder: {source_folder}")

        if not os.path.exists(replica_folder):
            os.makedirs(replica_folder)
            logging.info(f"Created replica folder: {replica_folder}")

        # Walk through the source folder and copy files and subfolders to the replica folder
        for root, dirs, files in os.walk(source_folder):
            # Calculate relative paths
            relative_path = os.path.relpath(root, source_folder)
            replica_path = os.path.join(replica_folder, relative_path)

            # Create subfolders in the replica folder if they don't exist
            for dir_name in dirs:
                source_dir = os.path.join(root, dir_name)
                replica_dir = os.path.join(replica_path, dir_name)
                if not os.path.exists(replica_dir):
                    os.makedirs(replica_dir)
                    logging.info(f"Created folder: {replica_dir}")

            # Copy files to the replica folder
            for file_name in files:
                source_file = os.path.join(root, file_name)
                replica_file = os.path.join(replica_path, file_name)
                shutil.copy2(source_file, replica_file)
                logging.info(f"Copied: {source_file} to {replica_file}")

        # Remove files and folders in the replica folder that do not exist in the source folder
        for root, dirs, files in os.walk(replica_folder):
            for dir_name in dirs:
                replica_dir = os.path.join(root, dir_name)
                source_dir = os.path.join(source_folder, os.path.relpath(replica_dir, replica_folder))
                if not os.path.exists(source_dir):
                    shutil.rmtree(replica_dir)
                    logging.warning(f"Removed folder: {replica_dir}")

            for file_name in files:
                replica_file = os.path.join(root, file_name)
                source_file = os.path.join(source_folder, os.path.relpath(replica_file, replica_folder))
                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    logging.warning(f"Removed file: {replica_file}")

        logging.info("Synchronization complete.")

        # Wait for the specified interval before the next synchronization
        time.sleep(interval_seconds)

def main():
    parser = argparse.ArgumentParser(description="Folder synchronization script.")
    parser.add_argument("source_folder", help="Path to the source folder")
    parser.add_argument("replica_folder", help="Path to the replica folder")
    parser.add_argument("interval_seconds", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")

    args = parser.parse_args()

    synchronize_folders(
        args.source_folder,
        args.replica_folder,
        args.interval_seconds,
        args.log_file
    )

if __name__ == "__main__":
    main()
"""

python main.py /path/to/source/folder /path/to/replica/folder 60 sync_log.txt



#Synchronization must be one-way: after the synchronization content of the replica folder should be modified to exactly 
match content of the source T
folder;
#Synchronization should be performed periodically. T
#File creation/copying/removal operations should be logged to a file and to the
console output; F
#Folder paths, synchronization interval and log file path should be provided
using the command line arguments; F
#It is undesirable to use third-party libraries that implement folder
synchronization; T
#It is allowed (and recommended) to use external libraries implementing other
well-known algorithms. For example, there is no point in implementing yet
another function that calculates MD5 if you need it for the task – it is
perfectly acceptable to use a third-party (or built-in) library. T
"""