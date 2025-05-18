import argparse
import shutil
from pathlib import Path

from app_integrator import core, extractor, desktop_entry


def main():
    parser = argparse.ArgumentParser(description="Intégrateur d'AppImage")
    parser.add_argument("appimage", nargs="?", help="Chemin vers le fichier .AppImage à intégrer")
    parser.add_argument("--uninstall", metavar="FICHIER", help="Désinstalle une AppImage (nom du fichier dans ~/Applications)")
    parser.add_argument("--list", action="store_true", help="Liste les AppImages intégrées")
    parser.add_argument("--info", metavar="FICHIER", help="Affiche les détails d'une AppImage intégrée")

    args = parser.parse_args()

    # Désinstallation
    if args.uninstall:
        removed = core.uninstall_appimage(args.uninstall)
        if removed:
            print("[✓] Éléments supprimés :")
            for r in removed:
                print(f" - {r}")
        else:
            print("[!] Aucun fichier trouvé à supprimer.")
        return
    
    # Liste
    if args.list:
        installed = core.list_installed_appimages()
        if not installed:
            print("[!] Aucune AppImage intégrée trouvée.")
            return
        
        print("[✓] AppImages intégrées :")
        for item in installed:
            print(f"- {item['name']}")
            print(f"  ↳ .desktop : {'✅' if item['desktop_exists'] else '❌'}")
            print(f"  ↳ icône   : {'✅' if item['icon_exists'] else '❌'}")
        return
    
    # Infos

    if args.info:
        info = core.get_appimage_info(args.info)
        print("[ℹ️] Détails de l’AppImage :")

        if info["appimage_path"]:
            print(f"  📦 AppImage : {info['appimage_path']}")
        else:
            print("  📦 AppImage : ❌ introuvable")

        if info["desktop_path"]:
            print(f"  🧾 .desktop : {info['desktop_path']}")
            print("  ── Contenu :")
            print(info["desktop_content"])
        else:
            print("  🧾 .desktop : ❌ introuvable")

        if info["icon_path"]:
            print(f"  🖼️ Icône    : {info['icon_path']}")
        else:
            print("  🖼️ Icône    : ❌ introuvable")

        return
    
    # Intégration
    if not args.appimage:
        print("[!] Veuillez spécifier un fichier .AppImage.")
        return

    file_path = Path(args.appimage).expanduser().resolve()

    try:
        print("[✓] Vérification du fichier...")
        if not core.is_appimage(file_path):
            raise ValueError("Ce fichier n'est pas une AppImage valide.")

        print("[✓] Déplacement dans ~/Applications...")
        moved_path = core.move_appimage(file_path)

        print("[✓] Extraction temporaire...")
        extracted_dir = extractor.extract_appimage(moved_path)

        print("[✓] Recherche d’icône...")
        icon_path = extractor.find_icon_in_extract_dir(extracted_dir)

        final_icon = None
        if icon_path:
            icon_dest_dir = Path.home() / ".local/share/icons"
            icon_dest_dir.mkdir(parents=True, exist_ok=True)
            final_icon = icon_dest_dir / f"{moved_path.stem}.png"
            shutil.copy2(icon_path, final_icon)
            print(f"[✓] Icône copiée : {final_icon}")
        else:
            print("[!] Aucune icône trouvée, une valeur générique sera utilisée.")

        print("[✓] Génération du fichier .desktop...")
        desktop_entry_path = desktop_entry.generate_desktop_entry(
            moved_path,
            icon_name=str(final_icon) if final_icon else None
        )

        print(f"[✅] Intégration terminée : {desktop_entry_path}")

    except Exception as e:
        print(f"[❌] Erreur : {e}")


if __name__ == "__main__":
    main()
