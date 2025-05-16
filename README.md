# ExpanSubi

ExpanSubi is a powerful text expansion utility built with Python that enables quick insertion of text snippets, templates, and dynamic content. It monitors your keyboard input and replaces predefined shortcuts with longer text snippets instantly.

## Features

- **Text Expansion**: Type custom shortcuts (like `:sign`) that automatically expand into longer text snippets
- **Dynamic Variables**: Insert date/time values automatically using variables like `{{date}}`, `{{time}}`, `{{datetime}}`
- **Easy Management**: Add, edit, and delete shortcuts through a simple GUI
- **Import/Export**: Share your shortcuts with colleagues by importing and exporting to JSON files
- **System Integration**: Option to start with Windows (Linux support coming soon)
- **Notification Control**: Toggle notifications for app actions

## Requirements

- Python 3.6 or higher
- Required Python packages (see `requirements.txt`)

## Installation

### Linux Support (New)

This repository includes ongoing work to improve Linux compatibility. The application was originally designed for Windows but is being adapted for Linux environments.

### Steps

1. Clone this repository:
   ```
   git clone https://github.com/RodriHaro/expansubi.git
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

## Usage

### Creating Shortcuts

1. Click the "Add" button
2. Enter your shortcut trigger text (e.g., `:sign`)
3. Enter the expanded text you want to appear when you type the shortcut
4. Click "Save"

### Using Dynamic Variables

You can insert the following variables in your expanded text:

- `{{date}}` - Current date (DD/MM/YYYY)
- `{{time}}` - Current time (HH:MM)
- `{{datetime}}` - Current date and time
- `{{year}}` - Current year
- `{{month}}` - Current month
- `{{day}}` - Current day
- `{{hour}}` - Current hour
- `{{minute}}` - Current minute

### Example

Shortcut: `:sign`
Expanded text: `Best regards,\nJohn Doe\nSent on {{date}} at {{time}}`

When you type `:sign` in any application, it will be replaced with:
```
Best regards,
John Doe
Sent on 16/05/2025 at 14:30
```

## Troubleshooting

### Linux-specific issues

- The auto-start feature is designed for Windows and may not work on Linux
- Some keyboard combinations may differ between operating systems
- For any issues, please open a GitHub issue with details

## Contributing

Contributions are welcome! Feel free to submit pull requests for bug fixes or new features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.