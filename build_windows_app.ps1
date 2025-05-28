# Universal Markdown Converter - Windows Build Script
# PowerShell version for better error handling

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Universal Markdown Converter - Windows Build" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pip is available
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: pip is not available" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing required dependencies..." -ForegroundColor Yellow

try {
    pip install -r requirements.txt
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Failed to install dependencies" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Building Windows executable..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray

try {
    # Clean previous builds
    if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
    if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
    
    # Build using PyInstaller
    pyinstaller --clean universal_md_converter.spec
    
    if (Test-Path "dist\Universal_Markdown_Converter.exe") {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "BUILD COMPLETED SUCCESSFULLY!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "The executable has been created:" -ForegroundColor White
        Write-Host "  📁 dist\Universal_Markdown_Converter.exe" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "You can now:" -ForegroundColor White
        Write-Host "  1. Run the executable directly" -ForegroundColor Gray
        Write-Host "  2. Copy it to any Windows computer (no Python required)" -ForegroundColor Gray
        Write-Host "  3. Create a desktop shortcut" -ForegroundColor Gray
        Write-Host ""
        
        # Get file size
        $fileSize = (Get-Item "dist\Universal_Markdown_Converter.exe").Length / 1MB
        Write-Host "File size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray
        
    } else {
        throw "Executable not found after build"
    }
    
} catch {
    Write-Host "✗ ERROR: Build failed" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Read-Host "Press Enter to exit"
