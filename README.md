# Expandeer

Expandeer is a text expander application for Linux and Windows, developed in Python with Tkinter and pynput.

## Main features
- Expansion of custom text shortcuts.
- Modern and simple graphical interface.
- Import/export of shortcuts in JSON format.
- Dynamic variables: {{date}}, {{time}}, {{datetime}}, {{year}}, etc.
- Clipboard integration and global functionality.
- Desktop launcher and applications menu integration.

## System-wide installation (recommended)

### 1. Download and install Expandeer for all users

Open a terminal and run:

```bash
wget https://raw.githubusercontent.com/RodriHaro/expandeer/main/expandeer_system_installer.sh
bash expandeer_system_installer.sh
```

This will install Expandeer for all users, add the launcher to the applications menu, and create the `expandeer` command for the terminal.

### 2. Run Expandeer

Search for "Expandeer" in your applications menu or run `expandeer` from any terminal.

## Requirements
- Debian/Ubuntu/Mint or compatible system
- sudo privileges

## Troubleshooting
- If the tray icon does not appear, make sure your desktop environment supports system tray icons.
- If the launcher doesn't appear, run `sudo update-desktop-database` or restart your session.
- If the clipboard doesn't work, make sure you have `xclip` installed.

## Credits
Developed by RH, 2025.