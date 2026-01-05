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
    print(f"[RUN] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"[OK] {description} 成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} 失败: {e}")
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
            print(f"[CLEAN] 清理 {dir_name} 目录")

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"[CLEAN] 删除 {file_name}")

    return True

def build_executable():
    """构建可执行文件"""
    system = platform.system().lower()

    # 使用简化的PyInstaller命令，不依赖复杂的spec文件
    cmd = "pyinstaller --clean --onefile --hidden-import=ddddocr --hidden-import=flask_cors --hidden-import=waitress --hidden-import=cv2 --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=numpy --hidden-import=sklearn main.py"

    success = run_command(cmd, "构建可执行文件")

    # 重命名生成的文件
    if success and os.path.exists("dist/main.exe" if system == "windows" else "dist/main"):
        exe_name = "OCR_Service.exe" if system == "windows" else "OCR_Service"
        dist_exe = os.path.join("dist", exe_name)
        os.rename("dist/main.exe" if system == "windows" else "dist/main", dist_exe)
        print(f"[OK] 生成文件已重命名为: {dist_exe}")

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
            print(f"[SUCCESS] 构建成功! 可执行文件: {exe_path}")
            print(f"[INFO] 文件大小: {file_size:.2f} MB")
            print("[USAGE] 使用说明:")
            print("   1. 将此文件复制到任何安装了相同操作系统类型的电脑上")
            print("   2. 双击运行即可启动OCR服务")
            print("   3. 服务将在 http://127.0.0.1:5000 启动")
            return True

    print("[ERROR] 未找到生成的可执行文件")
    return False

def main():
    """主函数"""
    print("开始打包OCR服务...")
    print(f"当前系统: {platform.system()} {platform.release()}")
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
            print(f"\n[ERROR] {step_name} 失败，停止构建")
            sys.exit(1)

    print(f"\n{'='*50}")
    print("打包完成！")
    print("现在你可以将生成的可执行文件分享给其他人使用了。")

if __name__ == "__main__":
    main()
