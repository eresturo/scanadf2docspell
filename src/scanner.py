import re
from os import system
from pathlib import Path

from src.page import Page


class Scanner:
    def __init__(self, config):
        self.config = config
        self.scan_folder = Path('scans')
        self.scan_folder.mkdir(exist_ok=True)

    def scan(self, front=True):
        suffix = ''
        if self.config.manual_duplex:
            suffix = '_front' if front else '_back'
        filename = f'"{self.config.name}"_%04d{suffix}.{self.config.scan_format}'
        filepath = self.scan_folder / filename
        source = f'"{self.config.source}"'
        adf_mode = f'Duplex' if self.config.duplex else Simplex
        color_mode = 'Color' if self.config.color else 'Gray'
        print(f'scan all pages using color mode: "{color_mode}" and source: {source} ...')
        device_filter = f'-d {self.config.device}' if self.config.device else ''

        batch_promt = '--batch-prompt' if self.config.manual_document_feeder else ''
        batch_start = f'--batch-start {self.config.start_count}' if self.config.start_count else ''
        scan_command = f'scanimage {device_filter} --mode {color_mode} --source {source} --adf-mode {adf_mode} --resolution {self.config.resolution} {batch_start} --batch={filepath} {batch_promt} --format {self.config.scan_format}'

        print(scan_command)
        system(scan_command)

    def get_pages(self):
        pages = []
        if self.config.manual_duplex:
            front_pages = sorted(
                file.name for file in Path('scans').glob(f'{self.config.name}_*_front.{self.config.scan_format}'))
            back_pages = sorted(
                (file.name for file in Path('scans').glob(f'{self.config.name}_*_back.{self.config.scan_format}')),
                reverse=True)
            if len(front_pages) != len(back_pages):
                raise AssertionError('Same number of front and back pages needed!')
            for i in range(len(front_pages)):
                pages.append(Page(front_pages[i], is_backside=False))
                pages.append(Page(back_pages[i], is_backside=True))
        else:
            for file in sorted(Path('scans').glob(f'{self.config.name}_*.{self.config.scan_format}')):
                is_backside = bool(re.match(rf'.*_\d{{3}}[02468].{self.config.scan_format}', file.name))
                pages.append(Page(file.name, is_backside=is_backside))
        if not pages:
            raise FileNotFoundError(
                'no scans found! Seems like scanimage produced no output? Check your setup / scanner.')
        return pages
