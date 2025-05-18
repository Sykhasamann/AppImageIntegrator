#!/bin/bash

APPDIR="/opt/appimage-integrator"
ICON_NAME="appimage-integrator.png"
ICON_DEST="/usr/share/icons/hicolor/256x256/apps"
DESKTOP_DEST="/usr/share/applications"
DESKTOP_FILE="appimage-integrator.desktop"
OPEN_DESKTOP_FILE="appimage-integrator-open.desktop"
WRAPPER_SCRIPT="$APPDIR/appimage-integrator-launch.sh"

echo "🔧 [POSTINST] Installation du raccourci et de l’icône..."

# 📝 Copier le .desktop principal
if [ -f "$APPDIR/$DESKTOP_FILE" ]; then
    echo "📝 Copie du .desktop vers $DESKTOP_DEST"
    cp "$APPDIR/$DESKTOP_FILE" "$DESKTOP_DEST/"
else
    echo "❌ .desktop introuvable dans $APPDIR"
fi

# 🖼️ Copier l'icône
if [ -f "$APPDIR/icon.png" ]; then
    echo "🖼️  Copie de l’icône vers $ICON_DEST/$ICON_NAME"
    mkdir -p "$ICON_DEST"
    cp "$APPDIR/icon.png" "$ICON_DEST/$ICON_NAME"
else
    echo "❌ Icône introuvable dans $APPDIR/icon.png"
fi

# 🔁 Créer le launcher pour clic droit
echo "🧩 Installation du launcher clic droit..."
cat << 'EOF' > "$WRAPPER_SCRIPT"
#!/bin/bash
python3 /opt/appimage-integrator/launch_gui.py "\$1"
EOF
chmod +x "$WRAPPER_SCRIPT"

# 🧾 Créer le .desktop d'ouverture avec
echo "📄 Enregistrement du .desktop d'intégration..."
cat << EOF > "$DESKTOP_DEST/$OPEN_DESKTOP_FILE"
[Desktop Entry]
Name=AppImage Integrator (Integrate)
Exec=$WRAPPER_SCRIPT "%f"
Type=Application
MimeType=application/x-executable;
NoDisplay=true
Icon=appimage-integrator
Categories=Utility;
EOF

# 🔄 Mise à jour des caches
echo "🔄 Mise à jour des caches..."
update-desktop-database "$DESKTOP_DEST" >/dev/null 2>&1 || true
gtk-update-icon-cache -f -t /usr/share/icons/hicolor >/dev/null 2>&1 || true

echo "✅ [POSTINST] Terminé : raccourci, icône et clic droit installés."