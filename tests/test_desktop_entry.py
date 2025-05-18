import unittest
import tempfile
from pathlib import Path
from app_integrator import desktop_entry


class TestDesktopEntry(unittest.TestCase):

    def test_generate_desktop_entry_creates_file(self):
        """
        Vérifie que le fichier .desktop est bien généré et contient les bonnes infos.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_appimage = Path(temp_dir) / "MyApp.AppImage"
            fake_appimage.write_text("#!/bin/bash\necho 'Hello'")
            fake_appimage.chmod(0o755)

            # Générer l'entrée .desktop
            desktop_path = desktop_entry.generate_desktop_entry(fake_appimage)

            self.assertTrue(desktop_path.exists())
            content = desktop_path.read_text()

            self.assertIn("Name=MyApp", content)
            self.assertIn("Exec=", content)
            self.assertIn("Icon=appimagekit_MyApp", content)
            self.assertIn("[Desktop Entry]", content)

            # Nettoyage du .desktop
            desktop_path.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
