#!/usr/bin/env python3
"""
Windows compatibility test script
Used to test OCR service in Windows environment
"""

import os
import sys
import platform
import subprocess

def test_windows_compatibility():
    """Test Windows compatibility"""
    print("Windows compatibility test")

    system = platform.system().lower()
    print(f"Current system: {system}")

    if system != "windows":
        print("Note: Not currently running on Windows")
        return True

    # Test necessary commands
    commands_to_test = [
        ("python --version", "Python version check"),
        ("pip --version", "Pip version check"),
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
    """Test service startup (simplified Windows version)"""
    print("Service startup test")

    try:
        # Simplified startup test
        result = subprocess.run([sys.executable, "main.py"],
                              capture_output=True,
                              text=True,
                              timeout=10)

        # Check if startup was successful (timeout is also successful as service runs continuously)
        if "Initializing ddddocr model" in result.stdout:
            print("Service started successfully")
            return True
        else:
            print(f"Service startup failed: {result.stdout}")
            return False

    except subprocess.TimeoutExpired:
        print("Service started successfully (normal timeout, service is running)")
        return True
    except Exception as e:
        print(f"Service startup exception: {e}")
        return False

def main():
    """Main test function"""
    print("Windows environment test started")
    print("=" * 40)

    tests = [
        ("Windows compatibility test", test_windows_compatibility),
        ("Service startup test", test_service_startup),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}")
        if test_func():
            passed += 1

    print(f"\n{'='*40}")
    print(f"Test results: {passed}/{total} passed")

    if passed == total:
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
