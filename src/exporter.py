from pathlib import Path

import img2pdf
import requests


class Exporter:
    def __init__(self, config):
        self.config = config

    def save_as_jpg(self, page):
        if page.removed:
            return
        page.load_image(load_processed=True)
        page.processed_filename = page.filename.replace(f'.{self.config.scan_format}', '.jpg')
        page.image.save(filename=Path('scans') / page.processed_filename)

    def save_as_pdf(self, pages):
        print('combine to one pdf...')
        a4 = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
        layout_fun_a4 = img2pdf.get_layout_fun(pagesize=a4)
        image_names = [str(Path('scans') / page.processed_filename) for page in pages if not page.removed]
        with open(Path('scans') / f'{self.config.name}.pdf', "wb") as f:
            f.write(img2pdf.convert(image_names, layout_fun=layout_fun_a4, viewer_center_window=True))

    def upload_doc(self):
        print('upload to docspell ...')
        url = f'{self.config.docspell_url}/api/v1/open/upload/item/{self.config.api_key}'
        return_value = requests.post(url, files={
            'file': open(Path('scans') / f'{self.config.name}.pdf', 'rb')
        })
        if return_value.status_code != 200:
            print(f'Could not upload doc, because of error {return_value.status_code}: {return_value.content}')
            return {}
        else:
            print('Upload ok :)')
