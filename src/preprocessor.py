import sys

from tqdm import tqdm

from src.exporter import Exporter


class Preprocessor:
    def __init__(self, config):
        self.config = config
        self.exporter = Exporter(config)

    def process(self, pages):
        for page in tqdm(pages, file=sys.stdout, desc='Preprocess all pages...'):
            self._process_image(page)

    def _process_image(self, page):
        page.load_image()
        if not self.config.skip_length_trimming:
            self._crop_height_dina4_ratio(page)
        if (self.config.duplex or self.config.manual_duplex) \
                and page.is_backside \
                and not self.config.skip_backside_rotation:
            self._rotate_page(page)
        if not self.config.skip_trim_pages:
            self._trim_image(page)
        if not self.config.skip_empty_page_removal:
            self._remove_page_if_empty(page)
        self.exporter.save_as_jpg(page)
        page.unload_image()

    def _remove_page_if_empty(self, page):
        empty_threshold = 100 * page.image.standard_deviation / page.image.quantum_range
        if empty_threshold < self.config.empty_threshold:
            page.removed = True
            print(f'remove blank page: {page.filename} because {empty_threshold} < {self.config.empty_threshold}')

    @staticmethod
    def _crop_height_dina4_ratio(page):
        ratio = 210.0 / 297.0
        height = int(page.image.width / ratio)
        if height < page.image.height:
            page.image.crop(0, 0, width=page.image.width, height=height)

    @staticmethod
    def _rotate_page(page):
        page.image.rotate(180)

    @staticmethod
    def _trim_image(page):
        page.image.trim(fuzz=0.2 * page.image.quantum_range, color='white')
