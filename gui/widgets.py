from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QTextEdit, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QPixmap
from pathlib import Path

from app_integrator.config_manager import set_config_value, get_config_value

from app_integrator import core, extractor, desktop_entry
from app_integrator.watcher import DownloadWatcher
import shutil


class MainWindow(QWidget):
    appimage_detected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AppImage Integrator")
        self.setFixedSize(400, 600)

        self.selected_file = None

    # Widgets principaux
        self.label = QLabel(QCoreApplication.translate("MainWindow", "Aucun fichier sélectionné"))
        self.label.setAlignment(Qt.AlignCenter)

        self.select_button = QPushButton(QCoreApplication.translate("MainWindows", "Choisir un fichier .AppImage"))
        self.select_button.clicked.connect(self.select_file)

        self.integrate_button = QPushButton(QCoreApplication.translate("MainWindows", "Intégrer"))
        self.integrate_button.setEnabled(False)
        self.integrate_button.clicked.connect(self.integrate_appimage)

        self.icon_preview = QLabel()
        self.icon_preview.setFixedSize(64, 64)
        self.icon_preview.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setText(QCoreApplication.translate("MainWindows", "🔍 Surveillance de ~/Téléchargements activée"))

        source = get_config_value("source_dir")
        target = get_config_value("target_dir")
        status = QCoreApplication.translate("MainWindow", "📥 Source : {}\n📦 Destination : {}").format(source, target)
        self.status_label.setText(status)


        self.list_button = QPushButton(QCoreApplication.translate("MainWindows", "Lister les AppImages intégrées"))
        self.list_button.clicked.connect(self.show_installed_list)

        self.list_area = QTextEdit()
        self.list_area.setReadOnly(True)
        self.list_area.setFixedHeight(100)

    # Liste interactive des AppImages installées
        self.appimage_list = QListWidget()
        self.appimage_list.setFixedHeight(150)
        self.appimage_list.itemSelectionChanged.connect(self.on_selection_changed)

        self.uninstall_button = QPushButton(QCoreApplication.translate("MainWindows", "Désinstaller"))
        self.uninstall_button.setEnabled(False)
        self.uninstall_button.clicked.connect(self.uninstall_selected_appimage)

    # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.integrate_button)
        layout.addWidget(self.icon_preview)
        layout.addWidget(self.status_label)
        layout.addWidget(self.list_button)
        layout.addWidget(self.list_area)
        layout.addWidget(self.appimage_list)
        layout.addWidget(self.uninstall_button)

    # Boutons de configuration des dossiers
        self.set_source_button = QPushButton(QCoreApplication.translate("MainWindow", "Définir le dossier source (.AppImage)"))
        self.set_source_button.clicked.connect(self.set_source_directory)

        self.set_target_button = QPushButton(QCoreApplication.translate("MainWindow", "Définir le dossier d’installation"))
        self.set_target_button.clicked.connect(self.set_target_directory)

        layout.addWidget(self.set_source_button)
        layout.addWidget(self.set_target_button)


        self.setLayout(layout)

    # Connexion du signal AppImage détectée
        self.appimage_detected.connect(self.handle_appimage_detected)

    # Lancement de la surveillance
        self.watcher = DownloadWatcher(self.on_appimage_detected)
        self.watcher.start()

    # Chargement initial de la liste d’AppImages installées
        self.refresh_appimage_list()

    def refresh_appimage_list(self):
        from app_integrator.core import list_installed_appimages

        self.appimage_list.clear()
        installed = list_installed_appimages()
        for item in installed:
            QListWidgetItem(item['name'], self.appimage_list)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            QCoreApplication.translate("MainWindow", "Sélectionner un fichier AppImage"),
            str(Path.home()),
            QCoreApplication.translate("MainWindow", "AppImage (*.AppImage)")
            )
        if file_path:
            self.selected_file = Path(file_path)
            self.label.setText(
                QCoreApplication.translate("MainWindow", "Sélectionné :") + f" {self.selected_file.name}"
                )
            self.integrate_button.setEnabled(True)
            self.status_label.setText("")

    def integrate_appimage(self):
        try:
            if not core.is_appimage(self.selected_file):
                raise ValueError(QCoreApplication.translate("MainWindow", "Le fichier sélectionné n'est pas une AppImage valide."))


            moved_path = core.move_appimage(self.selected_file)
            extracted_dir = extractor.extract_appimage(moved_path)
            icon_path = extractor.find_icon_in_extract_dir(extracted_dir)

            final_icon = None
            if icon_path:
                icon_dest = Path.home() / ".local/share/icons"
                icon_dest.mkdir(parents=True, exist_ok=True)
                final_icon = icon_dest / f"{moved_path.stem}.png"
                shutil.copy2(icon_path, final_icon)

            desktop_entry.generate_desktop_entry(moved_path, icon_name=str(final_icon) if final_icon else None)
            self.status_label.setText(QCoreApplication.translate("MainWindow", "✅ Intégration réussie !"))
        except Exception as e:
            self.status_label.setText(
                QCoreApplication.translate("MainWindow", "❌ Erreur : ") + str(e)
                )
            QMessageBox.critical(
                self,
                QCoreApplication.translate("MainWindow", "Erreur"),
                str(e)
                )

        if final_icon and final_icon.exists():
            pixmap = QPixmap(str(final_icon))
            self.icon_preview.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio))
        self.refresh_appimage_list()

    def show_installed_list(self):
        from app_integrator.core import list_installed_appimages

        installed = list_installed_appimages()
        if not installed:
            self.list_area.setText(
                QCoreApplication.translate("MainWindow", "Aucune AppImage intégrée.")
                )
            return

        output = ""
        for item in installed:
            output += f"- {item['name']}\n"
            output += "  " + QCoreApplication.translate("MainWindow", ".desktop") + " : "
            output += "✅\n" if item['desktop_exists'] else "❌\n"
            output += "  " + QCoreApplication.translate("MainWindow", "icône") + "   : "
            output += "✅\n\n" if item['icon_exists'] else "❌\n\n"


        self.list_area.setText(output)

    def on_appimage_detected(self, event):
        self.appimage_detected.emit(str(event.path))

    def handle_appimage_detected(self, path):
        result = QMessageBox.question(
            self,
            QCoreApplication.translate("MainWindow", "AppImage détectée"),
            QCoreApplication.translate("MainWindow", "Nouvelle AppImage détectée :\n{path}\n\nSouhaitez-vous l'intégrer?").format(path=path),
            QMessageBox.Yes | QMessageBox.No
            )
        if result == QMessageBox.Yes:
            self.selected_file = Path(path)
            self.label.setText(
                QCoreApplication.translate("MainWindow", "Sélectionné :") + f" {self.selected_file.name}"
            )
            self.integrate_button.setEnabled(True)
            self.integrate_appimage()

    def on_selection_changed(self):
        selected = self.appimage_list.selectedItems()
        self.uninstall_button.setEnabled(bool(selected))


    def uninstall_selected_appimage(self):
        selected = self.appimage_list.selectedItems()
        if not selected:
            return

        filename = selected[0].text()

        confirm = QMessageBox.question(
            self,
            QCoreApplication.translate("MainWindow", "Confirmation"),
            QCoreApplication.translate("MainWindow", "Voulez-vous vraiment désinstaller :\n{filename} ?").format(filename=filename),
            QMessageBox.Yes | QMessageBox.No
            )

        if confirm == QMessageBox.Yes:
            removed = core.uninstall_appimage(filename)
            if removed:
                QMessageBox.information(
                    self,
                    QCoreApplication.translate("MainWindow", "Désinstallation"),
                    QCoreApplication.translate("MainWindow", "{filename} a été désinstallé.").format(filename=filename)
                    )
            else:
                QMessageBox.warning(
                self,
                QCoreApplication.translate("MainWindow", "Erreur"),
                QCoreApplication.translate("MainWindow", "Aucun fichier à supprimer.")
                )

        self.refresh_appimage_list()

    def set_source_directory(self):
        title = QCoreApplication.translate("MainWindow", "Choisir le dossier source (.AppImage)")
        dir_path = QFileDialog.getExistingDirectory(self, title)
        if dir_path:
            set_config_value("source_dir", dir_path)
            msg = QCoreApplication.translate("MainWindow", "📥 Source : {}").format(dir_path)
            self.status_label.setText(msg)

    def set_target_directory(self):
        title = QCoreApplication.translate("MainWindow", "Choisir le dossier d’installation")
        dir_path = QFileDialog.getExistingDirectory(self, title)
        if dir_path:
            set_config_value("target_dir", dir_path)
            msg = QCoreApplication.translate("MainWindow", "📦 Destination : {}").format(dir_path)
            self.status_label.setText(msg)