#!/usr/bin/env python3
"""
Cross-platform packaging script
Used to package OCR service into executable files
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, description):
    """Run command and display status"""
    print(f"[RUN] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"[OK] {description} successful")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def install_dependencies():
    """Install dependencies"""
    return run_command("pip install -r requirements.txt", "Install project dependencies")

def install_pyinstaller():
    """Install PyInstaller"""
    return run_command("pip install pyinstaller", "Install PyInstaller")

def clean_build():
    """Clean previous builds"""
    dirs_to_remove = ["build", "dist"]
    files_to_remove = ["OCR_Service.exe", "OCR_Service"]

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
            print(f"[CLEAN] Clean {dir_name} directory")

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"[CLEAN] Remove {file_name}")

    return True

def build_executable():
    """Build executable file"""
    system = platform.system().lower()

    # Use simplified PyInstaller command without complex spec files
    cmd = "pyinstaller --clean --onefile --hidden-import=ddddocr --hidden-import=flask_cors --hidden-import=waitress --hidden-import=cv2 --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=numpy --hidden-import=sklearn main.py"

    success = run_command(cmd, "Build executable file")

    # Rename generated file
    if success and os.path.exists("dist/main.exe" if system == "windows" else "dist/main"):
        exe_name = "OCR_Service.exe" if system == "windows" else "OCR_Service"
        dist_exe = os.path.join("dist", exe_name)
        os.rename("dist/main.exe" if system == "windows" else "dist/main", dist_exe)
        print(f"[OK] Generated file renamed to: {dist_exe}")

    return success

def check_result():
    """Check build results"""
    system = platform.system().lower()
    exe_name = "OCR_Service.exe" if system == "windows" else "OCR_Service"

    exe_paths = [
        os.path.join("dist", exe_name),
        exe_name
    ]

    for exe_path in exe_paths:
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"[SUCCESS] Build successful! Executable: {exe_path}")
            print(f"[INFO] File size: {file_size:.2f} MB")
            print("[USAGE] Usage instructions:")
            print("   1. Copy this file to any computer with the same OS type")
            print("   2. Double-click to start the OCR service")
            print("   3. Service will run on http://127.0.0.1:5000")
            return True

    print("[ERROR] Generated executable not found")
    return False

def main():
    """Main function"""
    print("Starting OCR service packaging...")
    print(f"Current system: {platform.system()} {platform.release()}")
    print()

    steps = [
        ("Clean old builds", clean_build),
        ("Install dependencies", install_dependencies),
        ("Install PyInstaller", install_pyinstaller),
        ("Build executable file", build_executable),
        ("Check results", check_result),
    ]

    for step_name, step_func in steps:
        print(f"\n{'='*50}")
        if not step_func():
            print(f"\n[ERROR] {step_name} failed, stopping build")
            sys.exit(1)

    print(f"\n{'='*50}")
    print("Packaging complete!")
    print("You can now share the generated executable with others.")

if __name__ == "__main__":
    main()
