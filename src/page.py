import re
from pathlib import Path

from wand.image import Image


class Page:
    def __init__(self, filename, duplex=False):
        self.filename = filename
        self.processed_filename = None
        self.is_backside = duplex and bool(re.match(r'.*_\d{3}[02468].ppm', filename))
        self.image = None
        self.removed = False

    def load_image(self, load_processed=False):
        if not self.image:
            filename = self.processed_filename if load_processed else self.filename
            self.image = Image(filename=Path('scans') / filename)

    def unload_image(self):
        del self.image
        self.image = None
