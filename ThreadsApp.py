from PyQt5.QtCore import QThread, pyqtSignal

from Recon.recon import *
from Recon.Directory.directory import check_brute_force

from Recon.Attack import wsubtakeover, wsubtakeover_path
from Recon.takeover import *
from WAF import proxy as p


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
            fetchjs(self.Recon_place)
        if self.is_par:
            Parameter(self.Recon_place)
        if self.is_screen:
            screenwin(self.Recon_place)

        self.finished.emit()


# Attack Thread

class ThreadAttackDirectory(QThread):
    finished = pyqtSignal()

    def __init__(self, search, name, url):
        super().__init__()
        self.search = search
        self.name = name
        self.new_url = url

    def run(self) -> None:
        check_brute_force(self.search, self.new_url, self.name)
        self.finished.emit()

        pass


class ThreadAttackTakeover(QThread):
    finished = pyqtSignal()

    def __init__(self, url, path=None, location_result=None):
        super().__init__()
        self.domain_url = url
        self.path = path
        self.result = location_result

    def run(self) -> None:
        if self.path is None:
            wsubtakeover(self.domain_url, self.result)
        else:
            wsubtakeover_path(self.path, self.result)

        self.finished.emit()

        pass


class ThreadWAF(QThread):
    finished = pyqtSignal()

    def __init__(self, ip=None, port=None):
        super().__init__()
        self.ip = ip
        self.port = port

    def run(self) -> None:
        p.mitmdump(["-s", p.__file__, "-p", "5000", "--listen-host", self.ip, "--mode", f"reverse:http://{self.ip}:{self.port}"])
        self.finished.emit()

        pass
