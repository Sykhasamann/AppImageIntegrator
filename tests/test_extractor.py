import unittest
import tempfile
import stat
from pathlib import Path
from app_integrator import extractor


class TestExtractor(unittest.TestCase):

    def create_fake_appimage(self, path):
        """
        Crée un faux fichier AppImage exécutable.
        """
        path.write_text("#!/bin/bash\necho 'Fake AppImage'")
        path.chmod(path.stat().st_mode | stat.S_IEXEC)

    def test_extraction_should_fail_cleanly(self):
        """
        Le test vérifie que l'extracteur échoue proprement avec un faux fichier AppImage.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_appimage = Path(temp_dir) / "test.AppImage"
            self.create_fake_appimage(fake_appimage)

            with self.assertRaises(RuntimeError):
                extractor.extract_appimage(str(fake_appimage))


if __name__ == '__main__':
    unittest.main()
