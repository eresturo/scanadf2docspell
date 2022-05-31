#!/usr/bin/env python3
import uuid

from configargparse import ArgParser

from src.exporter import Exporter
from src.preprocessor import Preprocessor
from src.scanner import Scanner
from src.utils import Utils


def main(config):
    scanner = Scanner(config)
    preprocessor = Preprocessor(config)
    utils = Utils(config)

    scanner.scan(front=True)
    if config.manual_duplex:
        print('rotate pages and press enter')
        input()
        scanner.scan(front=False)
    pages = scanner.get_pages()
    preprocessor.process(pages)
    exporter = Exporter(config)
    exporter.save_as_pdf(pages)
    if utils.show_preview():
        exporter.upload_doc()
    utils.clean_up(pages)


def validate_config(config):
    if config.manual_duplex and config.duplex:
        raise ValueError('Canot use automatic duplex and manual duplex together!')


if __name__ == '__main__':
    parser = ArgParser(description='Scan from ADF, preprocess and upload do Docspell.',
                       default_config_files=['defaults.conf', 'custom.conf'])
    parser.add('--api_key', required=True, help="Docspell's API KEY")
    parser.add('--docspell_url', required=True, help="Url to docspell, e.g. http://<docpsell_host>:7880/")
    parser.add('-n', '--name', type=str, default=uuid.uuid1(), help='Name of the scan. Default is a random String')
    parser.add('-d', '--duplex', action='store_true', help='Scan front and back pages')
    parser.add('-m', '--manual_duplex', action='store_true',
               help='Scan front pages using ADF. Manual rotate pages. Scan back pages using ADF.')
    parser.add('-f', '--flatbed', action='store_true',
               help='Manually scan one page after the other from flatbed.')
    parser.add('-c', '--color', action='store_true', help='Do a colored scan')
    parser.add('--keep_scans', action='store_true', help='Do not delete raw scans')
    parser.add('--keep_pdf', action='store_true', help='Do not delete combined pdf')
    parser.add('--empty_threshold', type=float,
               help='Threshold to determine if a page is empty. The emptier a document is, the smaller it\' value becomes.')
    parser.add('--device', help='Device name (e.g. SCANNER_ABC). Default: None (use systems default scanner)')
    parser.add('--resolution', help='Scan resolution in dpi')
    parser.add('--command_flatbed',
               help='scanimage option to perform a flatbed scan (it\'s depending on your scanner).')
    parser.add('--command_adf',
               help='scanimage option to perform a single-page adf scan (it\'s depending on your scanner).')
    parser.add('--command_duplex_adf',
               help='scanimage option to perform a duplex adf scan (it\'s depending on your scanner).')
    parser.add('--preview', help='Show a preview before uploading to docspell')
    parser.add('--skip_backside_rotation', action='store_true',
               help='In duplex mode backsides are rotated, so the scripts rotates them back. Enable this to skip rotation.')
    parser.add('--skip_trim_pages', action='store_true',
               help='By default the white border around pages will be removed. Enable this to skip trimming pages.')
    parser.add('--skip_empty_page_removal', action='store_true',
               help='By default empty pages are deleted. Enable this to skip empty page deletion.')
    parser.add('--skip_length_trimming', action='store_true',
               help='By default length of the scans is trimmed to DIN A4 ratio. Enable this to skip trimming page lengths.')
    parser.add('--start_count', type=int,
               help='Overwrite the first page number. Useful if the scan was canceled and you want to resume a scan.')
    parser.add('--scan_format', type=str, default='pnm',
               help='Specifies the format in which to scan. However, the format is only temporary, scans are always converted to jpg and then bundled as pdf.')
    args = parser.parse_args()
    validate_config(args)
    main(config=args)
