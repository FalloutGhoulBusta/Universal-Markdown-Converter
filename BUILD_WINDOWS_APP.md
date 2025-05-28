# Building Universal Markdown Converter as Windows Application

This guide explains how to convert the Python script into a standalone Windows executable (.exe) that can run on any Windows computer without requiring Python to be installed.

## Prerequisites

1. **Python 3.7 or higher** installed on Windows
2. **pip** (usually comes with Python)
3. Internet connection for downloading dependencies

## Quick Build (Recommended)

### Option 1: Using PowerShell (Recommended)
1. Open PowerShell as Administrator
2. Navigate to the project folder
3. Run the build script:
   ```powershell
   .\build_windows_app.ps1
   ```

### Option 2: Using Command Prompt
1. Open Command Prompt as Administrator
2. Navigate to the project folder
3. Run the build script:
   ```cmd
   build_windows_app.bat
   ```

## Manual Build Process

If you prefer to build manually or the scripts don't work:

### Step 1: Install Dependencies
```cmd
pip install -r requirements.txt
```

### Step 2: Create Icon (Optional)
```cmd
python create_icon.py
```

### Step 3: Build Executable
```cmd
pyinstaller --clean universal_md_converter.spec
```

## Build Output

After successful build, you'll find:
- **Executable**: `dist\Universal_Markdown_Converter.exe`
- **Size**: Approximately 15-25 MB
- **Dependencies**: All included (no Python required on target machine)

## Distribution

The generated executable (`Universal_Markdown_Converter.exe`) is completely portable:

✅ **Can run on any Windows computer**  
✅ **No Python installation required**  
✅ **No additional dependencies needed**  
✅ **Can be copied to USB drives**  
✅ **Can be shared via email/cloud**  

## Troubleshooting

### Build Fails
- Ensure Python and pip are in your PATH
- Run Command Prompt/PowerShell as Administrator
- Check internet connection for dependency downloads

### Antivirus Warnings
- Some antivirus software may flag PyInstaller executables
- Add the `dist` folder to antivirus exclusions during build
- This is a false positive common with PyInstaller

### Large File Size
- The executable includes Python runtime and all dependencies
- Size is normal for PyInstaller builds (15-25 MB)
- Consider using UPX compression (included in spec file)

### Missing Icon
- If icon creation fails, the app will use Windows default icon
- Install Pillow for better icon: `pip install Pillow`
- You can manually replace `icon.ico` with your own

## Advanced Customization

### Custom Icon
Replace `icon.ico` with your own icon file (ICO format, multiple sizes recommended).

### Build Options
Edit `universal_md_converter.spec` to customize:
- Executable name
- Icon file
- Hidden imports
- Compression settings

### One-File vs One-Folder
Current build creates a single EXE file. For faster startup, you can modify the spec file to create a folder distribution.

## File Structure After Build

```
project/
├── universal_md_converter.py      # Source code
├── requirements.txt               # Dependencies
├── universal_md_converter.spec    # PyInstaller config
├── build_windows_app.bat         # Build script (CMD)
├── build_windows_app.ps1         # Build script (PowerShell)
├── create_icon.py                # Icon generator
├── icon.ico                      # Application icon
├── build/                        # Temporary build files
└── dist/
    └── Universal_Markdown_Converter.exe  # Final executable
```

## Usage of Built Application

1. Double-click `Universal_Markdown_Converter.exe`
2. The GUI will open automatically
3. Select markdown files or directories
4. Choose output format (HTML/PDF)
5. Optionally remove headers
6. Click Convert!

## Notes

- First run may be slower as Windows scans the new executable
- Chrome/Chromium is still required for PDF conversion
- The executable works offline for HTML conversion
- All original features are preserved in the Windows app
