import subprocess  # nosec
import sys
from pathlib import Path

from tqdm import tqdm


class Utils:
    def __init__(self, config):
        self.config = config

    def show_preview(self):
        if not self.config.preview:
            return True
        print("open preview...")
        subprocess.call(  # nosec
            ["xdg-open", Path("scans") / f"{self.config.name}.pdf"]
        )
        # Note: I know this is "unsafe", but I think there is no safer way...
        answer = ""
        while answer != "y" and answer != "n":
            print("Happy with the result? Upload? [y|n]: ")
            answer = input().lower()
        return answer == "y"

    @staticmethod
    def remove_if_exists(file):
        if file.exists():
            file.unlink()

    def clean_up(self, pages):
        scan_path = Path("scans")
        if not self.config.keep_pdf:
            print("Cleanup local pdf ...")
            self.remove_if_exists(scan_path / f"{self.config.name}.pdf")
        if not self.config.keep_scans:
            for page in tqdm(pages, file=sys.stdout, desc="Clean up all pages..."):
                page.unload_image()
                self.remove_if_exists(scan_path / page.filename)
                if page.processed_filename:
                    self.remove_if_exists(scan_path / page.processed_filename)
