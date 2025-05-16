#!/bin/bash
# Script de instalación automática para ExpanSubi en Linux
set -e

# Ruta del directorio actual
DIR="$(cd "$(dirname "$0")" && pwd)"

# 1. Instalar dependencias del sistema
sudo apt update
sudo apt install -y python3 python3-pip xclip

# 2. Instalar dependencias de Python
pip3 install --user -r "$DIR/requirements.txt"

# 3. Dar permisos de ejecución al lanzador
chmod +x "$DIR/expansubi.sh"

# 4. Copiar el archivo .desktop al menú de aplicaciones del usuario
DESKTOP_FILE="$DIR/expansubi.desktop"
MENU_DIR="$HOME/.local/share/applications"
mkdir -p "$MENU_DIR"

# Ajustar la ruta Exec en el .desktop si es necesario
sed "s|^Exec=.*|Exec=$DIR/expansubi.sh|" "$DESKTOP_FILE" > "$MENU_DIR/expansubi.desktop"
chmod +x "$MENU_DIR/expansubi.desktop"

echo "\n¡Instalación completada! Puedes buscar 'ExpanSubi' en tu menú de aplicaciones o ejecutar ./expansubi.sh desde la carpeta."
