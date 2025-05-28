@echo off
title Universal Markdown Converter - Build Windows App

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              Universal Markdown Converter                    ║
echo ║                Windows Application Builder                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Create icon first
echo [1/4] Creating application icon...
python create_icon.py

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Failed to install dependencies!
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo [3/4] Building Windows executable...
echo ⏳ This may take 2-5 minutes depending on your computer...
echo.

pyinstaller --clean universal_md_converter.spec

if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo [4/4] Verifying build...

if exist "dist\Universal_Markdown_Converter.exe" (
    echo.
    echo ╔══════════════════════════════════════════════════════════════╗
    echo ║                    🎉 BUILD SUCCESSFUL! 🎉                   ║
    echo ╚══════════════════════════════════════════════════════════════╝
    echo.
    echo ✅ Your Windows application is ready!
    echo.
    echo 📁 Location: dist\Universal_Markdown_Converter.exe
    echo 📊 Size: 
    for %%A in ("dist\Universal_Markdown_Converter.exe") do echo    %%~zA bytes
    echo.
    echo 🚀 What you can do now:
    echo    • Double-click the .exe to run it
    echo    • Copy it to any Windows computer
    echo    • Create a desktop shortcut
    echo    • Share it with others (no Python needed!)
    echo.
    
    REM Ask if user wants to run the app
    set /p choice="Would you like to run the application now? (y/n): "
    if /i "%choice%"=="y" (
        echo.
        echo 🚀 Launching Universal Markdown Converter...
        start "" "dist\Universal_Markdown_Converter.exe"
    )
    
) else (
    echo.
    echo ❌ Build completed but executable not found!
    echo Please check the build output above for errors.
)

echo.
echo Press any key to exit...
pause >nul
