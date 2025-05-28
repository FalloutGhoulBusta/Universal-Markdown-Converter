# Universal Markdown Converter

A comprehensive GUI application for converting Markdown files to HTML and PDF formats with professional styling and advanced features.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🖥️ **Easy-to-use GUI** - No command line required
- 📄 **Single file conversion** - Convert individual Markdown files
- 📁 **Batch conversion** - Process entire directories at once
- 🎨 **Professional styling** - Beautiful CSS with tables, code blocks, and more
- 📑 **Multiple formats** - Export to HTML or PDF
- 🚫 **Header removal option** - Remove auto-generated headers like "Generated on..."
- 🌐 **Cross-platform** - Works on Windows, macOS, and Linux
- 📦 **Portable** - Can be built as standalone Windows executable

## 🚀 Quick Start

### Option 1: Run Python Script
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python universal_md_converter.py
```

### Option 2: Build Windows Executable
```bash
# Double-click to build (Windows)
BUILD_EXE.bat

# Or use PowerShell
.\build_windows_app.ps1
```

## 📋 Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- markdown library (auto-installed)
- Chrome/Chromium (for PDF conversion)

## 🖼️ Screenshots

The application features a clean, intuitive interface with:
- File and directory selection
- Output format options (HTML/PDF)
- Header removal checkbox
- Progress tracking
- Detailed conversion log

## 📖 Usage

1. **Launch** the application
2. **Select** a Markdown file or directory
3. **Choose** output format (HTML or PDF)
4. **Optionally** remove headers using the checkbox
5. **Set** output directory (optional)
6. **Click** Convert!

## 🔧 Building Windows Executable

For users who want a standalone Windows application:

1. Run `BUILD_EXE.bat` (double-click)
2. Wait for the build to complete
3. Find your executable in the `dist` folder
4. Share the `.exe` file - no Python required!

See [BUILD_WINDOWS_APP.md](BUILD_WINDOWS_APP.md) for detailed instructions.

## 📁 Project Structure

```
universal-markdown-converter/
├── universal_md_converter.py      # Main application
├── requirements.txt               # Python dependencies
├── universal_md_converter.spec    # PyInstaller configuration
├── BUILD_EXE.bat                 # Simple build script
├── build_windows_app.ps1         # PowerShell build script
├── create_icon.py                # Icon generator
├── BUILD_WINDOWS_APP.md          # Build instructions
└── README.md                     # This file
```

## 🎯 Key Features Explained

### Header Removal
The application can remove auto-generated headers like:
- "Generated on 2025-05-28 18:42 | Print to PDF"
- Footer with converter attribution

Simply check the "Remove headers" checkbox before conversion.

### Professional Styling
- Clean, modern CSS design
- Responsive tables with hover effects
- Syntax-highlighted code blocks
- Print-optimized layouts
- Mobile-friendly responsive design

### Batch Processing
- Process entire directories of Markdown files
- Maintains folder structure
- Progress tracking for large batches
- Error handling for individual files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Issues & Support

If you encounter any issues or have feature requests:
1. Check existing issues on GitHub
2. Create a new issue with detailed description
3. Include your Python version and OS

## 🙏 Acknowledgments

- Built with Python and tkinter
- Uses the excellent `markdown` library
- PDF generation via Chrome/Chromium headless mode
- Executable creation with PyInstaller
