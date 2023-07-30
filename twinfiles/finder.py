"""
Find duplicated files based on their meta data.
"""
import hashlib
import os
from collections import defaultdict
from dataclasses import dataclass, field

from humanize import naturalsize
from rich import print
from rich.progress import MofNCompleteColumn, Progress, TimeElapsedColumn


@dataclass
class Finder:
    path: str
    file_stats: dict = field(default_factory=dict)
    same_sizes: dict = field(default_factory=dict)
    same_content: dict = field(default_factory=dict)

    def get_file_stats(self):
        total_size = 0
        self.path = os.path.expanduser(self.path)
        with Progress(
            MofNCompleteColumn(), *Progress.get_default_columns(), TimeElapsedColumn()
        ) as progress:
            task1 = progress.add_task("[cyan]Getting list of files...", total=None)
            for root, _, files in os.walk(self.path):
                for file_name in files:
                    progress.update(task1, advance=1)
                    full_filename = os.path.join(root, file_name)
                    file_stat = os.stat(full_filename)
                    self.file_stats[full_filename] = file_stat
                    total_size += file_stat.st_size

        self.total_str = f"Found {len(self.file_stats)} total file(s) using {naturalsize(total_size)}"

    def find_same_size(self):
        file_sizes: dict = defaultdict(list)

        with Progress(
            MofNCompleteColumn(), *Progress.get_default_columns()
        ) as progress:
            task1 = progress.add_task(
                "[cyan]Finding duplicate sizes...", total=len(self.file_stats)
            )
            for filename, filestat in self.file_stats.items():
                file_size = filestat.st_size
                progress.update(task1, advance=1)
                file_sizes[file_size].append(filename)

        self.same_sizes = {}
        total_duplicated_count = 0
        total_duplicated_size = 0
        for size, filesnames in file_sizes.items():
            dup_count = len(filesnames)
            if dup_count > 1:
                total_duplicated_count += dup_count - 1
                total_duplicated_size += (dup_count - 1) * size
                self.same_sizes[size] = filesnames

    def find_same_content(self):
        with Progress(
            MofNCompleteColumn(), *Progress.get_default_columns(), TimeElapsedColumn()
        ) as progress:
            total_duplicated_size = 0
            total_duplicated_count = 0
            task1 = progress.add_task(
                "[cyan]Finding duplicate content...", total=len(self.same_sizes)
            )
            for size, filename_list in self.same_sizes.items():
                progress.update(task1, advance=1)
                md5sum_dict = defaultdict(list)
                for filename in filename_list:
                    md5sum = self.calculate_md5sum(filename)
                    md5sum_dict[md5sum].append(filename)
                for md5sum, filenames in md5sum_dict.items():
                    if len(filenames) > 1:
                        self.same_content[md5sum] = filenames
                        total_duplicated_count += len(filenames) - 1
                        total_duplicated_size += (len(filenames) - 1) * size

        print(self.total_str)
        print(
            f"Found {total_duplicated_count} duplicated file(s) using {naturalsize(total_duplicated_size)}"
        )

    def delete(self):
        print("Deleting duplicated files...", end="", flush=True)
        for _, filenames in self.same_content.items():
            sorted_filenames = sorted(filenames)
            delete = sorted_filenames[1:]
            for filename in delete:
                os.remove(filename)
        print("Done")

    def list(self):
        print("Listing duplicated files...")
        for _, filenames in self.same_content.items():
            sorted_filenames = sorted(filenames)
            print(" ".join(sorted_filenames))

    @staticmethod
    def calculate_md5sum(file_path):
        md5_hash = hashlib.md5()

        with open(file_path, "rb") as file:
            # Read the file in small chunks to avoid memory issues with large files
            for chunk in iter(lambda: file.read(4096), b""):
                md5_hash.update(chunk)

        return md5_hash.hexdigest()
