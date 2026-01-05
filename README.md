# OCRdetect

一个基于ddddocr的验证码识别Flask API服务，支持图像预处理以提高识别准确率。可打包成Windows可执行文件，无需Python环境。

## 功能特点

- 🚀 基于ddddocr的高性能OCR识别
- 🖼️ 智能图像预处理（降噪、二值化、增强对比度）
- 🌐 跨域支持，适合油猴脚本调用
- 📦 支持打包成独立可执行文件，无需Python环境
- 🔄 自动测试和CI/CD支持

## 安装和运行

### 方法1：直接运行（需要Python环境）

```bash
# 安装依赖
pip install -r requirements.txt

# 运行服务
python main.py
```

### 方法2：打包成可执行文件（推荐）

#### Windows打包
```cmd
# 运行打包脚本
python build_exe.py

# 或在Windows上双击
build_exe.bat
```

打包完成后，会在 `dist/` 目录下生成 `OCR_Service.exe` 文件，可以直接在任何Windows电脑上运行，无需安装Python。

#### 其他平台
虽然主要针对Windows优化，但也可以在Linux/Mac上打包：
```bash
python build_exe.py
```

## API 使用

### POST /ocr

识别验证码图像

**请求示例：**
```javascript
fetch('http://127.0.0.1:5000/ocr', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    image: 'base64编码的图像数据'
  })
})
.then(response => response.json())
.then(data => {
  console.log('识别结果:', data.code);
});
```

**响应示例：**
```json
{
  "code": "XNH3ZB",
  "msg": "success"
}
```

## 项目结构

```
├── main.py              # 主服务文件
├── requirements.txt     # Python依赖
├── ocr_service.spec     # PyInstaller配置文件
├── build_exe.py         # 跨平台打包脚本
├── build_exe.bat        # Windows打包脚本
├── test_ocr.py          # 测试脚本
├── README.md           # 说明文档
└── .github/
    └── workflows/
        └── test.yml    # GitHub Actions配置
```

## 开发和测试

### 本地测试

```bash
# 运行测试
python test_ocr.py

# 测试特定图像
python test_ocr.py your_image.png
```

### GitHub Actions

项目配置了自动测试工作流，推送代码后会自动：

1. 在多种Python版本和操作系统上测试
2. 验证依赖安装
3. 测试OCR功能
4. 构建可执行文件

## 优化建议

如果识别准确率不理想，可以尝试：

1. **图像质量**：确保验证码清晰，无过多噪点
2. **对比度**：字符与背景要有足够对比度
3. **字符间距**：字符不要太密集或太分散
4. **字体大小**：字符大小适中

## 技术栈

- **后端框架**：Flask + Waitress
- **OCR引擎**：ddddocr
- **图像处理**：OpenCV + Pillow
- **打包工具**：PyInstaller
- **测试**：GitHub Actions

## 许可证

MIT License
# OCRdetect
# OCRdetect
