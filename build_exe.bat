@echo off
echo Building OCR Service Windows Executable...

REM 激活虚拟环境（如果有的话）
REM call venv\Scripts\activate.bat

REM 安装依赖
echo Installing dependencies...
pip install -r requirements.txt

REM 安装PyInstaller
pip install pyinstaller

REM 清理之前的构建
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist OCR_Service.exe del OCR_Service.exe

REM 使用PyInstaller打包
echo Building executable...
pyinstaller --clean --onefile ocr_service.spec

REM 检查构建结果
if exist dist\OCR_Service.exe (
    echo Build successful! Executable created at: dist\OCR_Service.exe
    echo You can copy this file to any Windows computer and run it directly.
) else (
    echo Build failed!
    exit /b 1
)

echo.
echo Build complete! The executable is ready to use.
pause
