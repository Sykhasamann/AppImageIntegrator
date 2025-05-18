import os
import subprocess
import shutil
import tempfile
from pathlib import Path

def extract_appimage(appimage_path):
    """
    Extrait le contenu de l'AppImage via plusieurs méthodes en cascade
    Retourne le chemin du dossier extrait ou monté.
    """

    extract_dir = Path(tempfile.mkdtemp(prefix="appimage_extract_"))

    # Méthode 1 : --appimage-extract

    if try_appimage_extract(appimage_path, extract_dir):
        return extract_dir / "squashfs-root"
    
    # Méthode 2 : squashfuse

    if try_squashfuse_mount(appimage_path, extract_dir):
        return extract_dir
    
    # Méthode 3 : bsdtar

    if try_bsdtar_extract(appimage_path, extract_dir):
        return extract_dir
    
    # Echec
    shutil.rmtree(extract_dir)
    raise RuntimeError("Impossible d'extraire l'AppImage avec les méthodes disponibles.")

def try_appimage_extract(appimage_path, extract_dir):
    try:
        result = subprocess.run(
            [appimage_path, "--appimage-extract"],
            cwd=extract_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return (extract_dir / "squashfs-root").exists()
    except Exception:
        return False
    
def try_squashfuse_mount(appimage_path, mount_point):
    try:
        subprocess.run(
            ["squashfuse", appimage_path, str(mount_point)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except Exception:
        return False
    
def try_bsdtar_extract(appimage_path, extract_dir):
    try:
        subprocess.run(
            ["bsdtar", "-xf", appimage_path, "-C", str(extract_dir)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except Exception:
        return False
    
def unmount_if_mounted(path):
    """Démonte un point de montage si nécessaire (ex: squashfuse.)"""
    if path.exists():
        subprocess.run(["fusermount", "-u", str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def find_icon_in_extract_dir(extracted_dir):
    """
    Recherche une icône réelle (.png/.svg) correspondant à l'Icon= dans un .desktop
    """
    import re

    icon_name = None

    print(f"[DEBUG] Analyse des fichiers dans : {extracted_dir}")

    for desktop_file in extracted_dir.glob("*.desktop"):
        print(f"[DEBUG] .desktop trouvé : {desktop_file}")
        content = desktop_file.read_text()
        for line in content.splitlines():
            if line.startswith("Icon="):
                icon_name = line.split("=", 1)[1].strip()
                print(f"[DEBUG] Icône déclarée dans .desktop : {icon_name}")
                break

    if not icon_name:
        print("[DEBUG] Aucun nom d'icône trouvé.")
        return None

    # On va chercher des fichiers .png/.svg qui correspondent
    possible_extensions = [".png", ".svg"]
    possible_paths = []

    for ext in possible_extensions:
        for size in ["256x256", "128x128", "64x64", "32x32", ""]:
            possible_paths.append(extracted_dir / f"usr/share/icons/hicolor/{size}/apps/{icon_name}{ext}")
        possible_paths.append(extracted_dir / f"usr/share/pixmaps/{icon_name}{ext}")

    for path in possible_paths:
        print(f"[DEBUG] Test : {path}")
        if path.exists():
            print(f"[DEBUG] Icône réelle trouvée : {path}")
            return path.resolve()

    print("[DEBUG] Aucune icône .png ou .svg trouvée avec ce nom.")
    return None


