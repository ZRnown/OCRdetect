import base64
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import ddddocr
import cv2
import numpy as np
from PIL import Image
import io

# 禁止 Flask 输出多余日志，只显示报错
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)  # 允许跨域，这样油猴脚本才能访问

print("正在初始化 ddddocr 模型... (首次运行可能需要下载模型)")
# 尝试多种模型配置以提高识别准确率
try:
    # 首先尝试标准模型
    ocr = ddddocr.DdddOcr(show_ad=False)
    print("✅ 使用标准 ddddocr 模型")
except Exception as e:
    print(f"标准模型加载失败，尝试其他配置: {e}")
    try:
        # 如果标准模型失败，尝试 old=True 参数
        ocr = ddddocr.DdddOcr(show_ad=False, old=True)
        print("✅ 使用旧版 ddddocr 模型")
    except Exception as e2:
        print(f"旧版模型也失败: {e2}")
        raise

print("✅ 模型加载完毕，OCR 服务已启动！监听端口 5000")

def preprocess_image(img_bytes):
    """图像预处理以提高 OCR 识别准确率"""
    try:
        # 将字节转换为 numpy 数组
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return img_bytes

        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 增强对比度
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)

        # 高斯模糊去噪
        blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)

        # 自适应二值化
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)

        # 形态学操作去除噪点
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # 转换为字节
        success, encoded_img = cv2.imencode('.png', cleaned)
        if success:
            return encoded_img.tobytes()
        else:
            return img_bytes

    except Exception as e:
        print(f"图像预处理失败，使用原图: {e}")
        return img_bytes

@app.route('/ocr', methods=['POST'])
def ocr_process():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'code': '', 'msg': 'No image data'}), 400

        # 获取 Base64 字符串
        img_base64 = data['image']

        # 解码为二进制
        img_bytes = base64.b64decode(img_base64)

        # 图像预处理以提高识别准确率
        processed_img_bytes = preprocess_image(img_bytes)

        # 尝试多种识别方式
        results = []

        # 1. 使用预处理后的图像识别
        try:
            res_code = ocr.classification(processed_img_bytes)
            results.append(('processed', res_code))
        except Exception as e:
            print(f"预处理图像识别失败: {e}")

        # 2. 使用原图识别作为备选
        try:
            original_code = ocr.classification(img_bytes)
            results.append(('original', original_code))
        except Exception as e:
            print(f"原图识别失败: {e}")

        if not results:
            return jsonify({'code': '', 'msg': 'OCR recognition failed'}), 500

        # 选择最可能的识别结果（这里简单选择第一个成功的）
        method, res_code = results[0]

        print(f"识别结果 [{method}]: {res_code}")
        
        print(f"识别成功: {res_code}")
        return jsonify({'code': res_code, 'msg': 'success'})

    except Exception as e:
        print(f"识别出错: {e}")
        return jsonify({'code': '', 'msg': str(e)}), 500

if __name__ == '__main__':
    # 使用 waitress 部署，比 flask 自带的 server 更稳定更快
    from waitress import serve
    serve(app, host='127.0.0.1', port=5000, threads=8)