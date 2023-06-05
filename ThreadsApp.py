from PyQt5.QtCore import QThread, pyqtSignal

from Recon.recon import *


# Recon Thread
class Thread(QThread):
    finished = pyqtSignal()
    subdomain = pyqtSignal()

    def __init__(self, domain=None,
                 is_live=None,
                 is_end=None,
                 is_par=None,
                 is_JS=None,
                 is_screen=None, path=None, url=None, project_place=None):
        super().__init__()
        self.is_screen = is_screen
        self.is_par = is_par
        self.is_JS = is_JS
        self.domain = domain
        self.is_live = is_live
        self.is_end = is_end
        self.is_running = True
        self.path = path
        self.url = url
        self.Recon_place = project_place

    def run(self) -> None:
        # super().sleep(1)
        if self.path is None:
            subfinder_for_single_windows(self.domain, self.Recon_place)
        else:
            subfinder_for_file_windows(self.path, self.Recon_place)

        if self.is_live:
            httprobe_w(self.Recon_place)

        if self.is_end:
            wwayback(self.Recon_place)
        if self.is_JS:
            if self.url is not None:
                fetchjs(self.url, self.Recon_place)
        if self.is_par:
            Parameter(self.Recon_place)
        if self.is_screen:
            screenwin(self.Recon_place)

        self.finished.emit()

# Attack Thread

class ThreadAttack(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        pass
