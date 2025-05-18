from pathlib import Path


DESKTOP_DIR = Path.home() / ".local/share/applications"


def generate_desktop_entry(appimage_path, app_name=None, icon_name=None, categories="Utility"):
    path = Path(appimage_path)
    name = app_name or path.stem
    exec_path = str(path.resolve())
    icon = str(Path(icon_name).resolve()) if icon_name else f"appimagekit_{name}"

    content = f"""[Desktop Entry]
Type=Application
Name={name}
Exec="{exec_path}"
Icon={icon}
Terminal=false
Categories={categories};
"""

    desktop_file = Path.home() / ".local/share/applications" / f"{name}.desktop"
    desktop_file.parent.mkdir(parents=True, exist_ok=True)
    desktop_file.write_text(content)
    desktop_file.chmod(0o755)

    return desktop_file
