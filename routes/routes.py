from flask import Blueprint, render_template, request, jsonify
import requests
import os
import time
import random

# 獲取 Hugging Face API 金鑰
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium-diffusers"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# 創建 Blueprint
routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        prompt = request.json.get('prompt')
        if not prompt:
            return jsonify({'error': '請輸入圖片描述'}), 400

        # 加入時間戳和隨機數
        timestamp = int(time.time())
        random_seed = random.randint(1, 1000000)
        
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "inputs": prompt,
                "parameters": {
                    "seed": random_seed,  # 添加隨機種子
                    "guidance_scale": 7.5,
                    "width": 1024,  # 設定圖片寬度
                    "height": 1024  # 設定圖片高度   # 可選參數
                }
            }
        )

        if response.status_code != 200:
            return jsonify({'error': 'API 請求失敗'}), response.status_code

        image_bytes = response.content
        # 使用時間戳來生成唯一的文件名
        image_path = os.path.join('static', 'images', f'generated_{timestamp}_{random_seed}.jpg')
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        
        with open(image_path, 'wb') as f:
            f.write(image_bytes)

        return jsonify({
            'success': True,
            'image_url': f'/{image_path}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500