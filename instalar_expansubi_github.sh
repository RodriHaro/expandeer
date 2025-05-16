#!/bin/bash
# Script de instalación y descarga automática para ExpanSubi desde GitHub
set -e

# 1. Instalar dependencias del sistema
sudo apt update
sudo apt install -y git python3 python3-pip xclip

# 2. Clonar el repositorio (en ~/expansubi o ruta personalizada)
DEST_DIR="$HOME/expansubi"
if [ -d "$DEST_DIR" ]; then
    echo "\nLa carpeta $DEST_DIR ya existe. ¿Deseas sobrescribirla? (s/n)"
    read -r resp
    if [ "$resp" != "s" ]; then
        echo "Instalación cancelada."
        exit 1
    fi
    rm -rf "$DEST_DIR"
fi
git clone https://github.com/RodriHaro/expansubi "$DEST_DIR"

cd "$DEST_DIR"

# 3. Instalar dependencias de Python
pip3 install --user -r requirements.txt

# 4. Dar permisos de ejecución al lanzador
chmod +x expansubi.sh

# 5. Copiar el archivo .desktop al menú de aplicaciones del usuario
DESKTOP_FILE="expansubi.desktop"
MENU_DIR="$HOME/.local/share/applications"
mkdir -p "$MENU_DIR"

# Ajustar la ruta Exec en el .desktop si es necesario
sed "s|^Exec=.*|Exec=$DEST_DIR/expansubi.sh|" "$DESKTOP_FILE" > "$MENU_DIR/expansubi.desktop"
chmod +x "$MENU_DIR/expansubi.desktop"

echo "\n¡Instalación completada! Puedes buscar 'ExpanSubi' en tu menú de aplicaciones o ejecutar ./expansubi.sh desde $DEST_DIR."
