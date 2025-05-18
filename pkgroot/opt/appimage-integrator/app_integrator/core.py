import os
import shutil
from pathlib import Path

from app_integrator.config_manager import get_config_value
APPLICATIONS_DIR = Path(get_config_value("target_dir"))


def is_appimage(file_path):

    """
    Vérifie si le fichier est une AppImage exécutable.
    """

    path = Path(file_path)
    return path.is_file() and path.suffix == ".AppImage" and os.access(path, os.X_OK)

def move_appimage(file_path):

    """
    Déplace l'AppImage vers ~/Applications si nécessaire.
    Si elle y est déjà, ne fait rien. Rend le fichier exécutable.
    Retourne le chemin final.
    """

    path = Path(file_path).resolve()
    if not is_appimage(path):
        raise ValueError(f"Fichier invalide ou non exécutable : {path}")

    APPLICATIONS_DIR.mkdir(parents=True, exist_ok=True)
    target_path = APPLICATIONS_DIR / path.name

    if path != target_path:
        print(f"[DEBUG] Déplacement de {path} vers {target_path}")
        shutil.move(str(path), str(target_path))
    else:
        print("[DEBUG] Fichier déjà dans Applications, déplacement ignoré.")

    target_path.chmod(0o755)
    return target_path

def uninstall_appimage(appimage_filename):
    
    """
    Supprimer le fichier AppImage, .desktop et icône associés.
    """

    from pathlib import Path

    app_dir = Path(get_config_value("target_dir"))
    desktop_dir = Path.home() / ".local/share/applications"
    icon_dir = Path.home() / ".local/share/icons"

    name = Path(appimage_filename).stem

    app_path = app_dir / appimage_filename
    desktop_path = desktop_dir / f"{name}.desktop"
    icon_path = icon_dir / f"{name}.png"

    removed = []

    for path in [app_path, desktop_path, icon_path]:
        if path.exists():
            path.unlink()
            removed.append(str(path))

    return removed

def list_installed_appimages():
    
    """
    Liste les AppImages présentes dans ~/Applications avec infos associées.
    """

    app_dir = Path(get_config_value("target_dir"))
    desktop_dir = Path.home() / ".local/share/applications"
    icon_dir = Path.home() / ".local/share/icons"

    if not app_dir.exists():
        return []
    
    items = []
    for file in app_dir.glob("*.AppImage"):
        name = file.stem
        desktop = desktop_dir / f"{name}.desktop"
        icon = icon_dir / f"{name}.png"

        items.append({
            "name": file.name,
            "desktop_exists": desktop.exists(),
            "icon_exists": icon.exists()
        })

    return items

def get_appimage_info(appimage_filename):
    
    """
    Retourne les informations liées à une AppImage intégrée.
    """

    app_dir = Path(get_config_value("target_dir"))
    desktop_dir = Path.home() / ".local/share/applications"
    icon_dir = Path.home() / ".local/share/icons"

    name = Path(appimage_filename).stem

    app_path = app_dir / appimage_filename
    desktop_path = desktop_dir / f"{name}.desktop"
    icon_path = icon_dir / f"{name}.png"

    info = {
        "appimage_path": app_path if app_path.exists() else None,
        "desktop_path": desktop_path if desktop_path.exists() else None,
        "icon_path": icon_path if icon_path.exists() else None,
        "desktop_content": None
    }

    if info["desktop_path"]:
        try:
            info["desktop_content"] = desktop_path.read_text()
        except Exception:
            info["desktop_content"] = "[Erreur lors de la lecture du fichier .desktop]"

    return info
