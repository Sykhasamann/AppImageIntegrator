from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app_integrator.config_manager import get_config_value
from pathlib import Path
import threading
import subprocess
import time

class AppImageDetectedEvent:
    def __init__(self, path):
        self.path = Path(path)

class DownloadWatcher(FileSystemEventHandler):
    def __init__(self, callback):

        """
        callback : fonction appelée avec un AppImage détecté
        """

        self.callback = callback
        self._observer = Observer()

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix == ".AppImage":
            time.sleep(1)  # attendre un peu pour que le fichier soit prêt
            self.callback(AppImageDetectedEvent(path))

    def get_download_dir(self):
        try:
            path = subprocess.check_output(["xdg-user-dir", "DOWNLOAD"]).decode().strip()
            return Path(path)
        except Exception:
            return Path.home() / "Downloads"  # Fallback

    def start(self, path=None):
        if path is None:
            path = Path(get_config_value("source_dir"))

        if not path.exists():
            print(f"[WATCHER] ❌ Dossier introuvable : {path}")
            return

        print(f"[WATCHER] ✅ Surveillance de : {path}")
        self._observer.schedule(self, str(path), recursive=False)
        thread = threading.Thread(target=self._observer.start, daemon=True)
        thread.start()



    def stop(self):
        self._observer.stop()
        self._observer.join()
