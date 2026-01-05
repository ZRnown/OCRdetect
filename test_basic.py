#!/usr/bin/env python3
"""
基础测试脚本，用于GitHub Actions
"""

import sys
import os

def test_imports():
    """测试所有必要的导入"""
    try:
        import flask
        import flask_cors
        import ddddocr
        import cv2
        import numpy
        import PIL
        from waitress import serve
        print("✅ 所有依赖导入成功")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_ocr_basic():
    """测试OCR基本功能"""
    try:
        import ddddocr
        import cv2
        import numpy as np

        ocr = ddddocr.DdddOcr(show_ad=False)

        # 创建一个简单的测试图像
        img = np.ones((50, 100, 3), dtype=np.uint8) * 255
        cv2.putText(img, 'ABC123', (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

        # 转换为字节
        success, encoded = cv2.imencode('.png', img)
        img_bytes = encoded.tobytes()

        # 测试识别
        result = ocr.classification(img_bytes)
        print(f"✅ OCR测试成功: {result}")
        return True
    except Exception as e:
        print(f"❌ OCR测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 开始基础测试...")

    tests = [
        ("依赖导入测试", test_imports),
        ("OCR功能测试", test_ocr_basic),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} 失败")

    print(f"\n{'='*30}")
    print(f"测试结果: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("❌ 部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
