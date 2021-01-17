import re
from os import system, listdir
from pathlib import Path

from src.page import Page


class Scanner:
    def __init__(self, config):
        self.config = config
        self.scan_folder = Path('scans')
        self.scan_folder.mkdir(exist_ok=True)

    def scan(self):
        filename = f'"{self.config.name}"_%04d.ppm'
        filepath = self.scan_folder / filename
        source = f'"{self.config.source_duplex}"' if self.config.duplex else self.config.source
        color_mode = 'Color' if self.config.color else 'Gray'
        print(f'scan all pages using color mode: "{color_mode}" and source: {source} ...')
        device_filter = f'-d {self.config.device}' if self.config.device else ''
        if self.config.flatbed:
            batch_start = f'--batch-start {self.config.start_count}' if self.config.start_count else ''
            scan_command = f'scanimage {device_filter} --mode {color_mode} --source Flatbed --resolution {self.config.resolution} {batch_start} --batch={filepath} --batch-prompt -x 210 -y 297'
        else:
            start_count = f'--start-count {self.config.start_count}' if self.config.start_count else ''
            scan_command = f'scanadf {device_filter} {start_count} --mode {color_mode} --source {source} --resolution {self.config.resolution} -o {filepath}'
        print(scan_command)
        system(scan_command)

    def get_pages(self):
        regex = re.compile(rf'{self.config.name}_\d{{4}}.ppm')
        sorted_filenames = sorted([file for file in listdir('scans') if regex.search(file)])
        if not sorted_filenames:
            raise FileNotFoundError(
                'no scans found! Seems like scanadf produced no output? Check your setup / scanner.')
        return [Page(file, duplex=self.config.duplex) for file in sorted_filenames]
