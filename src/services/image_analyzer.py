#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片智能分析服务 - 基于颜色和形状的简单识别
"""
from PIL import Image
from collections import Counter
import colorsys
import io

class ImageAnalyzer:
    """衣物图片分析器"""
    
    # 颜色名称映射（HSV范围 -> 颜色名称）
    COLOR_RANGES = {
        'red': [(0, 20), (340, 360)],      # 红色
        'orange': [(20, 40)],               # 橙色  
        'yellow': [(40, 70)],               # 黄色
        'green': [(70, 160)],               # 绿色
        'blue': [(160, 250)],               # 蓝色
        'purple': [(250, 290)],             # 紫色
        'pink': [(290, 340)],               # 粉色
    }
    
    # 颜色中文名映射
    COLOR_NAMES = {
        'red': '红色', 'orange': '橙色', 'yellow': '黄色',
        'green': '绿色', 'blue': '蓝色', 'purple': '紫色',
        'pink': '粉色', 'black': '黑色', 'white': '白色',
        'gray': '灰色', 'brown': '棕色', 'beige': '米色',
        'navy': '藏青'
    }
    
    # 衣物类型的默认温度范围
    TYPE_TEMP_RANGES = {
        'tops': {'min': 15, 'max': 35},       # 上衣：春秋夏
        'bottoms': {'min': 5, 'max': 35},     # 下装：全年
        'outerwear': {'min': -10, 'max': 20}, # 外套：秋冬
        'shoes': {'min': -10, 'max': 40},     # 鞋子：全年
        'accessories': {'min': -20, 'max': 40} # 配饰：全年
    }
    
    @classmethod
    def analyze(cls, image_file):
        """
        分析图片并返回识别结果
        
        Args:
            image_file: 文件对象或文件路径
            
        Returns:
            dict: {
                'suggested_type': 建议的衣物类型,
                'suggested_color': 建议的颜色,
                'dominant_colors': 主要颜色列表,
                'suggested_temp': {'min': 最低温度, 'max': 最高温度},
                'confidence': 置信度 (0-100)
            }
        """
        try:
            # 打开图片
            if hasattr(image_file, 'read'):
                image_file.seek(0)
                img = Image.open(image_file)
            else:
                img = Image.open(image_file)
            
            # 转换为RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 分析图片
            dominant_colors = cls._extract_dominant_colors(img)
            suggested_color = cls._get_color_name(dominant_colors[0] if dominant_colors else (128, 128, 128))
            suggested_type = cls._guess_clothing_type(img, dominant_colors)
            suggested_temp = cls.TYPE_TEMP_RANGES.get(suggested_type, {'min': 10, 'max': 30})
            
            # 计算置信度（基于颜色纯度和图片质量）
            confidence = cls._calculate_confidence(img, dominant_colors)
            
            return {
                'suggested_type': suggested_type,
                'suggested_color': suggested_color,
                'dominant_colors': [cls._rgb_to_hex(c) for c in dominant_colors[:3]],
                'suggested_temp': suggested_temp,
                'confidence': confidence
            }
            
        except Exception as e:
            # 返回默认值
            return {
                'suggested_type': 'tops',
                'suggested_color': 'black',
                'dominant_colors': ['#000000'],
                'suggested_temp': {'min': 15, 'max': 30},
                'confidence': 0,
                'error': str(e)
            }
    
    @classmethod
    def _extract_dominant_colors(cls, img, num_colors=5):
        """提取图片主要颜色"""
        # 缩小图片以加快处理速度
        img_small = img.resize((100, 100), Image.Resampling.LANCZOS)
        pixels = list(img_small.getdata())
        
        # 过滤掉太亮或太暗的像素（可能是背景）
        filtered_pixels = []
        for pixel in pixels:
            r, g, b = pixel[:3]
            # 计算亮度
            brightness = (r + g + b) / 3
            # 过滤纯白和纯黑背景
            if 20 < brightness < 240:
                filtered_pixels.append((r, g, b))
        
        if not filtered_pixels:
            filtered_pixels = [(r, g, b) for r, g, b, *_ in [p if len(p) >= 3 else (p[0], p[0], p[0]) for p in pixels[:100]]]
        
        # 对颜色进行量化（减少颜色数量）
        quantized = []
        for r, g, b in filtered_pixels:
            # 将颜色量化到32级
            qr = (r // 32) * 32
            qg = (g // 32) * 32
            qb = (b // 32) * 32
            quantized.append((qr, qg, qb))
        
        # 统计颜色频率
        color_counts = Counter(quantized)
        dominant = color_counts.most_common(num_colors)
        
        return [color for color, count in dominant]
    
    @classmethod
    def _get_color_name(cls, rgb):
        """根据RGB值获取颜色名称"""
        r, g, b = rgb
        
        # 转换到HSV空间
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        h = h * 360  # 转换为0-360度
        s = s * 100  # 转换为百分比
        v = v * 100
        
        # 检测黑白灰
        if v < 20:
            return 'black'
        if v > 85 and s < 15:
            return 'white'
        if s < 15:
            return 'gray'
        
        # 检测棕色和米色
        if 15 < h < 40 and 20 < s < 60 and 20 < v < 70:
            return 'brown'
        if 30 < h < 50 and 10 < s < 40 and 70 < v < 95:
            return 'beige'
        
        # 检测藏青色
        if 200 < h < 240 and s > 30 and 20 < v < 50:
            return 'navy'
        
        # 根据色相判断颜色
        for color_name, ranges in cls.COLOR_RANGES.items():
            for (low, high) in ranges:
                if low <= h < high:
                    return color_name
        
        return 'gray'  # 默认
    
    @classmethod
    def _guess_clothing_type(cls, img, dominant_colors):
        """根据图片特征猜测衣物类型"""
        width, height = img.size
        aspect_ratio = width / height
        
        # 获取主色调的特征
        if dominant_colors:
            main_color = dominant_colors[0]
            r, g, b = main_color
            brightness = (r + g + b) / 3
            
            # 转换为HSV
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            saturation = s * 100
        else:
            brightness = 128
            saturation = 50
        
        # 基于宽高比和颜色特征的简单启发式规则
        
        # 鞋子通常是横向的
        if aspect_ratio > 1.5:
            return 'shoes'
        
        # 裤子/下装通常是纵向的
        if aspect_ratio < 0.6:
            return 'bottoms'
        
        # 根据颜色饱和度和亮度进行进一步判断
        # 外套通常颜色较深或较中性
        if brightness < 80 and saturation < 40:
            return 'outerwear'
        
        # 配饰的判断（较小的物品，但这里无法判断实际大小）
        # 默认归类为上衣
        return 'tops'
    
    @classmethod
    def _calculate_confidence(cls, img, dominant_colors):
        """计算识别置信度"""
        confidence = 50  # 基础置信度
        
        # 图片质量加分
        width, height = img.size
        if width >= 200 and height >= 200:
            confidence += 15
        if width >= 400 and height >= 400:
            confidence += 10
        
        # 颜色清晰度加分
        if dominant_colors:
            main_color = dominant_colors[0]
            r, g, b = main_color
            # 颜色饱和度高说明图片主体清晰
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            if s > 0.3:
                confidence += 15
            if v > 0.3 and v < 0.9:
                confidence += 10
        
        return min(confidence, 100)
    
    @classmethod
    def _rgb_to_hex(cls, rgb):
        """RGB转十六进制颜色"""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)


# 便捷函数
def analyze_clothing_image(image_file):
    """分析衣物图片的便捷函数"""
    return ImageAnalyzer.analyze(image_file)
