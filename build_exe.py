#!/usr/bin/env python3
"""
跨平台打包脚本
用于将OCR服务打包成可执行文件
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, description):
    """运行命令并显示状态"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def install_dependencies():
    """安装依赖"""
    return run_command("pip install -r requirements.txt", "安装项目依赖")

def install_pyinstaller():
    """安装PyInstaller"""
    return run_command("pip install pyinstaller", "安装PyInstaller")

def clean_build():
    """清理之前的构建"""
    dirs_to_remove = ["build", "dist"]
    files_to_remove = ["OCR_Service.exe", "OCR_Service"]

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
            print(f"🗑️ 清理 {dir_name} 目录")

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"🗑️ 删除 {file_name}")

    return True

def build_executable():
    """构建可执行文件"""
    system = platform.system().lower()

    if system == "windows":
        spec_file = "ocr_service.spec"
    else:
        # 为非Windows系统创建简单的spec
        spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'ddddocr',
        'flask_cors',
        'waitress',
        'cv2',
        'PIL',
        'PIL.Image',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OCR_Service',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
        with open("ocr_service_temp.spec", "w") as f:
            f.write(spec_content)
        spec_file = "ocr_service_temp.spec"

    cmd = f"pyinstaller --clean --onefile {spec_file}"
    success = run_command(cmd, "构建可执行文件")

    # 清理临时spec文件
    if spec_file == "ocr_service_temp.spec" and os.path.exists(spec_file):
        os.remove(spec_file)

    return success

def check_result():
    """检查构建结果"""
    system = platform.system().lower()
    exe_name = "OCR_Service.exe" if system == "windows" else "OCR_Service"

    exe_paths = [
        os.path.join("dist", exe_name),
        exe_name
    ]

    for exe_path in exe_paths:
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"✅ 构建成功! 可执行文件: {exe_path}")
            print(f"📏 文件大小: {file_size:.2f} MB")
            print("📝 使用说明:")
            print("   1. 将此文件复制到任何安装了相同操作系统类型的电脑上")
            print("   2. 双击运行即可启动OCR服务")
            print("   3. 服务将在 http://127.0.0.1:5000 启动")
            return True

    print("❌ 未找到生成的可执行文件")
    return False

def main():
    """主函数"""
    print("🚀 开始打包OCR服务...")
    print(f"📍 当前系统: {platform.system()} {platform.release()}")
    print()

    steps = [
        ("清理旧构建", clean_build),
        ("安装依赖", install_dependencies),
        ("安装PyInstaller", install_pyinstaller),
        ("构建可执行文件", build_executable),
        ("检查结果", check_result),
    ]

    for step_name, step_func in steps:
        print(f"\n{'='*50}")
        if not step_func():
            print(f"\n❌ {step_name} 失败，停止构建")
            sys.exit(1)

    print(f"\n{'='*50}")
    print("🎉 打包完成！")
    print("现在你可以将生成的可执行文件分享给其他人使用了。")

if __name__ == "__main__":
    main()
