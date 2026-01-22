#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用配置文件
"""
import os

# 基础路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库配置
DATABASE_PATH = os.path.join(BASE_DIR, 'wardrobe.db')

# 上传配置
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# 衣服类型定义
CLOTHING_TYPES = {
    'tops': '上衣',
    'bottoms': '下装',
    'outerwear': '外套',
    'shoes': '鞋子',
    'accessories': '配饰'
}

# 温度范围定义（摄氏度）
TEMPERATURE_RANGES = {
    'very_cold': {'min': -20, 'max': 0, 'label': '严寒 (-20°C ~ 0°C)'},
    'cold': {'min': 0, 'max': 10, 'label': '寒冷 (0°C ~ 10°C)'},
    'cool': {'min': 10, 'max': 18, 'label': '凉爽 (10°C ~ 18°C)'},
    'mild': {'min': 18, 'max': 25, 'label': '温和 (18°C ~ 25°C)'},
    'warm': {'min': 25, 'max': 32, 'label': '温暖 (25°C ~ 32°C)'},
    'hot': {'min': 32, 'max': 45, 'label': '炎热 (32°C ~ 45°C)'}
}

# 穿搭风格
OUTFIT_STYLES = {
    'casual': '休闲',
    'formal': '正式',
    'sporty': '运动',
    'elegant': '优雅'
}

# 颜色选项
COLORS = {
    'black': '黑色',
    'white': '白色',
    'gray': '灰色',
    'red': '红色',
    'blue': '蓝色',
    'green': '绿色',
    'yellow': '黄色',
    'pink': '粉色',
    'purple': '紫色',
    'brown': '棕色',
    'beige': '米色',
    'navy': '藏青',
    'other': '其他'
}

# 天气API配置
WEATHER_API_KEY_FILE = os.path.join(BASE_DIR, 'backend', 'weather', '.api_key')
CITY_DATA_FILE = os.path.join(BASE_DIR, 'backend', 'weather', 'AMap_adcode_citycode.xlsx')
