#!/bin/bash
set -e

# 1. Instalar dependencias del sistema
sudo apt-get update
sudo apt-get install -y python3 python3-pip xclip git

# 2. Clonar o copiar la app a /opt/expandeer
sudo rm -rf /opt/expandeer
sudo git clone https://github.com/RodriHaro/expandeer.git /opt/expandeer

# 3. Instalar dependencias de Python globalmente
sudo pip3 install -r /opt/expandeer/requirements.txt pystray pillow pynput pyperclip

# 4. Crear lanzador de escritorio global
sudo cp /opt/expandeer/expandeer.desktop /usr/share/applications/expandeer.desktop
sudo sed -i 's|Exec=.*|Exec=/usr/local/bin/expandeer|' /usr/share/applications/expandeer.desktop
sudo sed -i 's|Icon=.*|Icon=/opt/expandeer/expandeer.png|' /usr/share/applications/expandeer.desktop

# 5. Crear symlink para ejecutar desde terminal (siempre apuntando al script real)
sudo ln -sf /opt/expandeer/expandeer.sh /usr/local/bin/expandeer
sudo chmod +x /opt/expandeer/expandeer.sh

# 6. Actualizar base de datos de lanzadores
sudo update-desktop-database

echo "Expandeer installed system-wide! Search for 'Expandeer' in your applications menu or run 'expandeer' from the terminal."
