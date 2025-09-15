import threading

from django.apps import AppConfig

from .features.Camera import Camera


class PyroAppConfig(AppConfig):
    name = "pyro"
    verbose_name = "Pyro"
    _startup_done = False

    def ready(self):
        if self._startup_done:
            return
        thread = threading.Thread(target=self.start_cameras, daemon=True)
        thread.start()
        self._startup_done = True

    def start_cameras(self):
        sources = [0]
        cameras = {}
        for source in sources:
            cameras[source] = Camera(source)
