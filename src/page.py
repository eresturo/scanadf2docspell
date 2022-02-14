from pathlib import Path

from wand.image import Image


class Page:
    def __init__(self, filename, is_backside=False):
        self.filename = filename
        self.processed_filename = None
        self.is_backside = is_backside
        self.image = None
        self.removed = False

    def load_image(self, load_processed=False):
        if not self.image:
            filename = self.processed_filename if load_processed else self.filename
            self.image = Image(filename=Path('scans') / filename)

    def unload_image(self):
        del self.image
        self.image = None
