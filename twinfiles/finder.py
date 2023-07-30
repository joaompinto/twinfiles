"""
Find duplicated files based on their meta data.
"""
import os
from collections import defaultdict
from dataclasses import dataclass, field

from rich.progress import MofNCompleteColumn, Progress


@dataclass
class Finder:
    path: str
    file_stats: dict = field(default_factory=dict)
    file_sizes: dict = field(default_factory=dict)

    def get_file_list(self):
        self.path = os.path.expanduser(self.path)
        with Progress(
            MofNCompleteColumn(), *Progress.get_default_columns()
        ) as progress:
            task1 = progress.add_task("[cyan]Getting list of files...", total=None)
            for root, _, files in os.walk(self.path):
                for file_name in files:
                    progress.update(task1, advance=1)
                    full_filename = os.path.join(root, file_name)
                    self.file_stats[full_filename] = os.stat(full_filename)

    def find_duplicates(self):
        file_sizes: dict = defaultdict(list)

        with Progress(
            MofNCompleteColumn(), *Progress.get_default_columns()
        ) as progress:
            task1 = progress.add_task("[cyan]Comparing...", total=len(self.file_stats))
            for filename, filestat in self.file_stats.items():
                file_size = filestat.st_size
                progress.update(task1, advance=1)
                file_sizes[file_size].append(filename)

        self.file_sizes = file_sizes

    @staticmethod
    def stat_cmp(stat1, stat2):
        return stat1.st_size == stat2.st_size
