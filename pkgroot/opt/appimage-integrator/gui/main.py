import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale

def main(preselected_file=None):
    app = QApplication(sys.argv)

    translator = QTranslator()
    locale = QLocale.system().name()

    base_path = Path(__file__).resolve().parent.parent
    i18n_dir = base_path / "i18n"
    qm_path = i18n_dir / f"{locale}.qm"

    print(f"[DEBUG] Tentative de chargement via fichier : {qm_path}")
    success = translator.load(str(qm_path))
    print(f"[DEBUG] Chargement réussi ? {success}")

    if success:
        app.installTranslator(translator)

    from gui.widgets import MainWindow
    window = MainWindow()

    if preselected_file:
        window.selected_file = preselected_file
        window.label.setText(f"Selected: {preselected_file.name}")
        window.integrate_button.setEnabled(True)

    window.show()
    sys.exit(app.exec_())

