# OCRdetect

A Flask API service for captcha recognition based on ddddocr, with image preprocessing to improve accuracy. Can be packaged into Windows executable files without requiring Python environment.

## Features

- High-performance OCR recognition based on ddddocr
- Smart image preprocessing (noise reduction, binarization, contrast enhancement)
- CORS support for userscript calls
- Support for packaging into standalone executable files without Python environment
- Automatic testing and CI/CD support

## Installation and Running

### Method 1: Direct run (requires Python environment)

```bash
# Install dependencies
pip install -r requirements.txt

# Run service
python main.py
```

### Method 2: Package into executable (recommended)

#### Windows packaging
```cmd
# Run packaging script
python build_exe.py

# Or double-click on Windows
build_exe.bat
```

After packaging, an `OCR_Service.exe` file will be generated in the `dist/` directory, which can be run directly on any Windows computer without installing Python.

#### Other platforms
Although primarily optimized for Windows, it can also be packaged on Linux/Mac:
```bash
python build_exe.py
```

## API Usage

### POST /ocr

Recognize captcha images

**Request example:**
```javascript
fetch('http://127.0.0.1:5000/ocr', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    image: 'base64-encoded image data'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Recognition result:', data.code);
});
```

**Response example:**
```json
{
  "code": "XNH3ZB",
  "msg": "success"
}
```

## Project Structure

```
├── main.py              # Main service file
├── requirements.txt     # Python dependencies
├── ocr_service.spec     # PyInstaller configuration
├── build_exe.py         # Cross-platform packaging script
├── build_exe.bat        # Windows packaging script
├── test_ocr.py          # Test script
├── README.md           # Documentation
└── .github/
    └── workflows/
        └── test.yml    # GitHub Actions configuration
```

## Development and Testing

### Local Testing

```bash
# Run tests
python test_basic.py

# Test specific image
python test_ocr.py your_image.png
```

### GitHub Actions

The project has automatic testing workflow configured. After pushing code, it will automatically:

1. Test on multiple Python versions and operating systems
2. Verify dependency installation
3. Test OCR functionality
4. Build executable files

## Optimization Suggestions

If recognition accuracy is not ideal, try:

1. **Image quality**: Ensure captcha is clear without excessive noise
2. **Contrast**: Characters should have sufficient contrast with background
3. **Character spacing**: Characters should not be too dense or too sparse
4. **Font size**: Character size should be moderate

## Technology Stack

- **Backend framework**: Flask + Waitress
- **OCR engine**: ddddocr
- **Image processing**: OpenCV + Pillow
- **Packaging tool**: PyInstaller
- **Testing**: GitHub Actions

## License

MIT License
# OCRdetect
# OCRdetect
