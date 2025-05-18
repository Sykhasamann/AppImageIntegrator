#!/bin/bash

APP_NAME="appimage-integrator"
VERSION="1.1.1"
OUTPUT_DIR="dist"
BUILD_DIR="pkgroot/opt/$APP_NAME"

mkdir -p "$BUILD_DIR/i18n" "$OUTPUT_DIR"

echo "📁 Copie des fichiers..."
cp -r gui app_integrator "$BUILD_DIR/"
cp launch_gui.py icon.png appimage-integrator.desktop "$BUILD_DIR/"
cp i18n/*.qm "$BUILD_DIR/i18n/"

echo "📦 Construction .deb..."
fpm -s dir -t deb \
  -n $APP_NAME \
  -v $VERSION \
  -C pkgroot \
  --after-install postinst.sh \
  --before-remove prerm \
  --depends "python3" \
  --depends "python3-pyqt5" \
  --depends "python3-watchdog" \
  -p $OUTPUT_DIR/${APP_NAME}_${VERSION}.deb

echo "📦 Construction .rpm..."
fpm -s dir -t rpm \
  -n $APP_NAME \
  -v $VERSION \
  -C pkgroot \
  --after-install postinst.sh \
  --before-remove prerm \
  --depends "python3" \
  --depends "python3-qt5" \
  --depends "python3-watchdog" \
  -p $OUTPUT_DIR/${APP_NAME}-${VERSION}.rpm

echo "✅ Paquets générés dans $OUTPUT_DIR/"
