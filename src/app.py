#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能穿搭推荐系统 - 主应用
"""
import os
import json
import uuid
from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
from werkzeug.utils import secure_filename
from datetime import timedelta

# 配置导入
from config import (
    BASE_DIR, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH,
    CLOTHING_TYPES, TEMPERATURE_RANGES, OUTFIT_STYLES, COLORS,
    WEATHER_API_KEY_FILE, CITY_DATA_FILE
)

# 模型和服务导入
from models.database import init_database, ClothingModel
from services.recommender import OutfitRecommender
from services.image_analyzer import analyze_clothing_image

# 天气API
from backend.weather.api import WeatherInformation, GetCityName

# 创建Flask应用
app = Flask(
    __name__,
    template_folder='./frontend/templates',
    static_folder='./static'
)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.send_file_max_age_default = timedelta(seconds=1)

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== 页面路由 ====================

@app.route('/')
def index():
    """主页 - 穿搭推荐"""
    return render_template('index.html')

@app.route('/wardrobe')
def wardrobe():
    """衣橱管理页面"""
    return render_template('wardrobe.html')

@app.route('/upload')
def upload_page():
    """上传页面"""
    return render_template('upload.html')

# ==================== API路由 ====================

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取配置信息"""
    return jsonify({
        'clothing_types': CLOTHING_TYPES,
        'temperature_ranges': TEMPERATURE_RANGES,
        'outfit_styles': OUTFIT_STYLES,
        'colors': COLORS
    })

@app.route('/api/clothing', methods=['GET'])
def get_clothing():
    """获取衣物列表"""
    clothing_type = request.args.get('type')
    items = ClothingModel.get_all(clothing_type)
    return jsonify({'success': True, 'data': items})

@app.route('/api/clothing', methods=['POST'])
def add_clothing():
    """添加衣物"""
    try:
        # 处理文件上传
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': '请上传图片'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'message': '请选择图片'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': f'不支持的图片格式，仅支持: {ALLOWED_EXTENSIONS}'}), 400
        
        # 获取表单数据
        name = request.form.get('name', '').strip()
        clothing_type = request.form.get('type', '').strip()
        color = request.form.get('color', '')
        style = request.form.get('style', '')
        temp_min = int(request.form.get('temp_min', 0))
        temp_max = int(request.form.get('temp_max', 40))
        description = request.form.get('description', '')
        
        if not name or not clothing_type:
            return jsonify({'success': False, 'message': '名称和类型不能为空'}), 400
        
        if clothing_type not in CLOTHING_TYPES:
            return jsonify({'success': False, 'message': '无效的衣物类型'}), 400
        
        # 保存文件
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        type_folder = os.path.join(UPLOAD_FOLDER, clothing_type)
        os.makedirs(type_folder, exist_ok=True)
        
        file_path = os.path.join(type_folder, unique_filename)
        file.save(file_path)
        
        # 相对路径用于存储和访问
        relative_path = f"uploads/{clothing_type}/{unique_filename}"
        
        # 保存到数据库
        clothing_id = ClothingModel.add(
            name=name,
            clothing_type=clothing_type,
            color=color,
            style=style,
            temp_min=temp_min,
            temp_max=temp_max,
            image_path=relative_path,
            description=description
        )
        
        return jsonify({
            'success': True, 
            'message': '添加成功',
            'data': {'id': clothing_id, 'image_path': relative_path}
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'添加失败: {str(e)}'}), 500

@app.route('/api/clothing/<int:clothing_id>', methods=['DELETE'])
def delete_clothing(clothing_id):
    """删除衣物"""
    try:
        item = ClothingModel.get_by_id(clothing_id)
        if not item:
            return jsonify({'success': False, 'message': '衣物不存在'}), 404
        
        # 删除图片文件
        if item.get('image_path'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], '..', item['image_path'])
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # 删除数据库记录
        ClothingModel.delete(clothing_id)
        return jsonify({'success': True, 'message': '删除成功'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'删除失败: {str(e)}'}), 500

@app.route('/api/recommend', methods=['GET', 'POST'])
def get_recommendation():
    """获取穿搭推荐"""
    try:
        # 获取参数
        if request.method == 'POST':
            data = request.get_json() or {}
            temperature = data.get('temperature')
            city = data.get('city')
            style = data.get('style')
        else:
            temperature = request.args.get('temperature')
            city = request.args.get('city')
            style = request.args.get('style')
        
        # 如果提供了城市，获取实时天气
        weather_data = None
        if city:
            weather_response = WeatherInformation(city)
            if weather_response.get('status') == '1' and weather_response.get('lives'):
                weather_data = weather_response['lives'][0]
                temperature = float(weather_data.get('temperature', 25))
        
        if temperature is None:
            temperature = 25  # 默认温度
        else:
            temperature = float(temperature)
        
        # 获取推荐
        recommendations = OutfitRecommender.recommend(temperature, style, count=3)
        
        # 构建响应
        response = {
            'success': True,
            'temperature': temperature,
            'weather': weather_data,
            'recommendations': recommendations,
            'tips': OutfitRecommender.OUTFIT_RULES.get(
                OutfitRecommender.get_temperature_level(temperature), {}
            ).get('tips', '')
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取推荐失败: {str(e)}'}), 500

@app.route('/api/wardrobe/summary', methods=['GET'])
def get_wardrobe_summary():
    """获取衣橱概况"""
    try:
        summary = OutfitRecommender.get_wardrobe_summary()
        return jsonify({'success': True, 'data': summary})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/weather/view', methods=['GET'])
def get_weather():
    """获取天气信息"""
    city_name = request.args.get('city', '上海市')
    weather_data = WeatherInformation(city_name)
    weather_json_str = json.dumps(weather_data, ensure_ascii=False)
    resp = make_response(weather_json_str)
    resp.headers['Content-Type'] = 'application/json; charset=UTF-8'
    return resp

@app.route('/api/weather/cities', methods=['GET'])
def get_cities():
    """获取城市列表"""
    city_list = GetCityName()
    return jsonify(city_list)

# ==================== 静态文件服务 ====================

@app.route('/static/uploads/<path:filename>')
def uploaded_file(filename):
    """提供上传的文件"""
    return send_from_directory(UPLOAD_FOLDER, filename)

# ==================== 初始化 ====================

def initialize():
    """应用初始化"""
    # 确保上传目录存在
    for clothing_type in CLOTHING_TYPES.keys():
        type_folder = os.path.join(UPLOAD_FOLDER, clothing_type)
        os.makedirs(type_folder, exist_ok=True)
    
    # 初始化数据库
    init_database()
    print("✅ 应用初始化完成")

if __name__ == '__main__':
    initialize()
    app.run(host='0.0.0.0', port=5000, debug=True)
