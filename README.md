
# AppImage Integrator

**AppImage Integrator** est une application graphique et en ligne de commande pour faciliter l'installation, la gestion et la suppression de fichiers `.AppImage` sous Linux.

![AppImage Integrator](https://img.shields.io/badge/status-stable-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Languages](https://img.shields.io/badge/languages-fr--FR%20%7C%20en--US-yellow)

## ✨ Fonctionnalités

- 📂 Intégration automatique d'un fichier `.AppImage`
- 🔎 Détection en temps réel de nouveaux fichiers dans le dossier Téléchargements
- 🧹 Désinstallation propre avec suppression des entrées `.desktop` et icônes
- 🧾 Génération automatique de fichiers `.desktop`
- 🖼️ Gestion des icônes de l'application
- 🌍 Interface multilingue (Français 🇫🇷 / Anglais 🇬🇧)
- ⚙️ Personnalisation du dossier source et de destination
- 🧪 Mode CLI ou interface graphique (`PyQt5`)

## 📦 Installation

### Fedora / RHEL / dérivés

```bash
sudo dnf install ./appimage-integrator-1.2.rpm
```

### Debian / Ubuntu / dérivés

```bash
sudo apt install ./appimage-integrator_1.2.deb
```

## 🖥️ Lancement
Interface graphique :
```bash
appimage-integrator
```
Ou bien via le menu des applications.

Ligne de commande :

```bash
appimage-integrator /chemin/vers/fichier.AppImage
appimage-integrator --list
appimage-integrator --uninstall NomDuFichier.AppImage
appimage-integrator --info NomDuFichier.AppImage
```

## 🌐 Traduction
L'application détecte automatiquement la langue système.

Traductions disponibles :

    Français (par défaut)
    Anglais
Vous pouvez forcer la langue via :
```bash
LANG=en_US.UTF-8 appimage-integrator
```

## ⚙️ Configuration

Le fichier de configuration est stocké dans :
```bash
~/.config/appimage-integrator/config.json
```
Il contient les chemins source et destination des AppImages. Vous pouvez également les modifier depuis l’interface graphique.

## 🔧 Dépendances

🔧 Dépendances

- Python 3.7+
- PyQt5
- watchdog

Installées automatiquement avec le paquet .deb ou .rpm.

## 📃 Licence
Ce projet est sous licence MIT.
Développé avec ❤️ par syks.








