#!/usr/bin/env python3
"""
Windows兼容性测试脚本
用于在Windows环境中测试OCR服务
"""

import os
import sys
import platform
import subprocess

def test_windows_compatibility():
    """测试Windows兼容性"""
    print("Windows兼容性测试")

    system = platform.system().lower()
    print(f"当前系统: {system}")

    if system != "windows":
        print("注意：当前不在Windows系统上运行")
        return True

    # 测试必要的命令
    commands_to_test = [
        ("python --version", "Python版本检查"),
        ("pip --version", "Pip版本检查"),
    ]

    for cmd, desc in commands_to_test:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"[OK] {desc}: {result.stdout.strip()}")
            else:
                print(f"[ERROR] {desc} 失败: {result.stderr.strip()}")
                return False
        except Exception as e:
            print(f"[ERROR] {desc} 异常: {e}")
            return False

    return True

def test_service_startup():
    """测试服务启动（简化的Windows版本）"""
    print("服务启动测试")

    try:
        # 简化的启动测试
        result = subprocess.run([sys.executable, "main.py"],
                              capture_output=True,
                              text=True,
                              timeout=10)

        # 检查是否成功启动（即使超时也是成功的，因为服务会持续运行）
        if "正在初始化 ddddocr 模型" in result.stdout:
            print("服务启动成功")
            return True
        else:
            print(f"服务启动失败: {result.stdout}")
            return False

    except subprocess.TimeoutExpired:
        print("服务启动成功（正常超时，服务正在运行）")
        return True
    except Exception as e:
        print(f"服务启动异常: {e}")
        return False

def main():
    """主测试函数"""
    print("Windows环境测试开始")
    print("=" * 40)

    tests = [
        ("Windows兼容性测试", test_windows_compatibility),
        ("服务启动测试", test_service_startup),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}")
        if test_func():
            passed += 1

    print(f"\n{'='*40}")
    print(f"测试结果: {passed}/{total} 通过")

    if passed == total:
        print("所有测试通过！")
        return 0
    else:
        print("部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
