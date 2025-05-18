from pathlib import Path
import subprocess

def get_download_dir():
    try:
        path = subprocess.check_output(["xdg-user-dir", "DOWNLOAD"]).decode().strip()
        return Path(path)
    except Exception as e:
        print(f"[⚠] Erreur lors de l'appel à xdg-user-dir : {e}")
        return Path.home() / "Downloads"

# Test du chemin détecté
download_dir = get_download_dir()
print(f"[✅] Dossier téléchargements détecté : {download_dir}")

# Vérifie si le dossier existe vraiment
if download_dir.exists() and download_dir.is_dir():
    print("[✅] Le dossier existe bien.")
else:
    print("[❌] Le dossier n'existe pas !")
