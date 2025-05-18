
# AppImage Integrator

**AppImage Integrator** is a graphical, command-line application for easy installation, management and removal of `.AppImage` files under Linux.

![AppImage Integrator](https://img.shields.io/badge/status-stable-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Languages](https://img.shields.io/badge/languages-fr--FR%20%7C%20en--US-yellow)

## ✨ Features

- 📂 Automatic integration of `.AppImage` files
- 🔎 Real-time detection of new files in the Downloads folder
- 🧹 Clean uninstall with removal of `.desktop` entries and icons
- 🧾 Automatic generation of `.desktop` files
- 🖼️ Application icon management
- 🌍 Multilingual interface (French 🇫🇷 / English 🇬🇧)
- ⚙️ Source and destination folder customization
- 🧪 CLI mode or graphical user interface (`PyQt5`)

## 📦 Installation

### Fedora / RHEL / derivates

```bash
sudo dnf install ./appimage-integrator-1.2.rpm
```

### Debian / Ubuntu / derivates

```bash
sudo apt install ./appimage-integrator_1.2.deb
```

## 🖥️ Launch
Graphical interface :
```bash
appimage-integrator
```
Or via the applications menu.

Command line :

```bash
appimage-integrator /chemin/vers/fichier.AppImage
appimage-integrator --list
appimage-integrator --uninstall NomDuFichier.AppImage
appimage-integrator --info NomDuFichier.AppImage
```

## 🌐 Translation
The application automatically detects the system language.

Available translations :

    French (default)
    English
You can force the language with :
```bash
LANG=en_US.UTF-8 appimage-integrator
```

## ⚙️ Configuration

The configuration file is stored in :
```bash
~/.config/appimage-integrator/config.json
```
It contains the source and destination paths for AppImages. You can also modify them from the graphical interface.

## 🔧 Dependencies

🔧 Dependencies

- Python 3.7+
- PyQt5
- watchdog

Automatically installed with the .deb or .rpm package.

## 📃 Licence
This project is licensed by MIT.
Developed with ❤️ by syks.








