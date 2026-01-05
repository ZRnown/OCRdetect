#!/usr/bin/env python3
"""
Basic test script for GitHub Actions
"""

import sys
import os

def test_imports():
    """Test all necessary imports"""
    try:
        import flask
        import flask_cors
        import ddddocr
        import cv2
        import numpy
        import PIL
        from waitress import serve
        print("All dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"Import failed: {e}")
        return False

def test_ocr_basic():
    """Test basic OCR functionality"""
    try:
        import ddddocr
        import cv2
        import numpy as np

        ocr = ddddocr.DdddOcr(show_ad=False)

        # Create a simple test image
        img = np.ones((50, 100, 3), dtype=np.uint8) * 255
        cv2.putText(img, 'ABC123', (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

        # Convert to bytes
        success, encoded = cv2.imencode('.png', img)
        img_bytes = encoded.tobytes()

        # Test recognition
        result = ocr.classification(img_bytes)
        print(f"OCR test successful: {result}")
        return True
    except Exception as e:
        print(f"OCR test failed: {e}")
        return False

def main():
    """Main test function"""
    print("Starting basic tests...")

    tests = [
        ("Dependency import test", test_imports),
        ("OCR functionality test", test_ocr_basic),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}")
        if test_func():
            passed += 1
        else:
            print(f"{test_name} failed")

    print(f"\n{'='*30}")
    print(f"Test results: {passed}/{total} passed")

    if passed == total:
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
