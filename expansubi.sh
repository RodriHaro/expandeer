#!/bin/bash
# Script para lanzar ExpanSubi en Linux

# Directorio del script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Activar entorno virtual si existe
if [ -f "$DIR/venv/bin/activate" ]; then
    source "$DIR/venv/bin/activate"
fi

# Ejecutar la app principal
python3 linux_app.py
