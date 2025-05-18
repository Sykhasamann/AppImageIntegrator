import unittest
import tempfile
import stat
from pathlib import Path
from app_integrator import core


class TestCore(unittest.TestCase):

    def create_fake_appimage(self, path):
        """
        Crée un faux fichier AppImage exécutable.
        """
        path.write_text("#!/bin/bash\necho 'Fake AppImage'")
        path.chmod(path.stat().st_mode | stat.S_IEXEC)

    def test_is_appimage_true(self):
        """
        Vérifie que le fichier est reconnu comme AppImage valide.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            appimage = Path(temp_dir) / "test.AppImage"
            self.create_fake_appimage(appimage)
            self.assertTrue(core.is_appimage(appimage))

    def test_move_appimage(self):
        """
        Teste le déplacement de l'AppImage vers ~/Applications.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            appimage = Path(temp_dir) / "move_test.AppImage"
            self.create_fake_appimage(appimage)

            target_path = core.move_appimage(appimage)

            self.assertTrue(target_path.exists())
            self.assertTrue(target_path.is_file())
            self.assertTrue(target_path.stat().st_mode & stat.S_IEXEC)

            # Nettoyage : supprimer le fichier copié dans ~/Applications
            target_path.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
