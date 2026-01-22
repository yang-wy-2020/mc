#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
穿搭推荐服务
"""
import random
from models.database import ClothingModel
from config import TEMPERATURE_RANGES, CLOTHING_TYPES

class OutfitRecommender:
    """穿搭推荐引擎"""
    
    # 穿搭规则：不同温度下需要的衣物类型
    OUTFIT_RULES = {
        'very_cold': {
            'required': ['tops', 'bottoms', 'outerwear', 'shoes'],
            'optional': ['accessories'],
            'layers': 3,  # 建议层数
            'tips': '严寒天气，建议多层穿搭，注意保暖'
        },
        'cold': {
            'required': ['tops', 'bottoms', 'outerwear', 'shoes'],
            'optional': ['accessories'],
            'layers': 2,
            'tips': '寒冷天气，建议穿厚外套'
        },
        'cool': {
            'required': ['tops', 'bottoms', 'shoes'],
            'optional': ['outerwear', 'accessories'],
            'layers': 2,
            'tips': '凉爽天气，可搭配轻薄外套'
        },
        'mild': {
            'required': ['tops', 'bottoms', 'shoes'],
            'optional': ['accessories'],
            'layers': 1,
            'tips': '温和天气，穿着舒适即可'
        },
        'warm': {
            'required': ['tops', 'bottoms', 'shoes'],
            'optional': ['accessories'],
            'layers': 1,
            'tips': '温暖天气，建议穿轻薄透气的衣物'
        },
        'hot': {
            'required': ['tops', 'bottoms', 'shoes'],
            'optional': ['accessories'],
            'layers': 1,
            'tips': '炎热天气，建议穿短袖短裤，注意防晒'
        }
    }
    
    @staticmethod
    def get_temperature_level(temperature):
        """根据温度获取温度等级"""
        temp = float(temperature)
        for level, range_info in TEMPERATURE_RANGES.items():
            if range_info['min'] <= temp < range_info['max']:
                return level
        # 边界处理
        if temp < -20:
            return 'very_cold'
        return 'hot'
    
    @classmethod
    def recommend(cls, temperature, style=None, count=3):
        """
        根据温度推荐穿搭组合
        
        Args:
            temperature: 当前温度（摄氏度）
            style: 期望风格（可选）
            count: 推荐组合数量
            
        Returns:
            list: 穿搭推荐列表
        """
        temp = float(temperature)
        temp_level = cls.get_temperature_level(temp)
        rules = cls.OUTFIT_RULES.get(temp_level, cls.OUTFIT_RULES['mild'])
        
        # 获取适合当前温度的所有衣物
        suitable_clothing = {}
        for clothing_type in CLOTHING_TYPES.keys():
            items = ClothingModel.get_by_temperature(temp, clothing_type)
            if style:
                items = [item for item in items if item.get('style') == style or not item.get('style')]
            suitable_clothing[clothing_type] = items
        
        # 生成推荐组合
        recommendations = []
        for i in range(count):
            outfit = {
                'id': i + 1,
                'items': {},
                'temp_level': temp_level,
                'tips': rules['tips'],
                'missing': []
            }
            
            # 必需的衣物类型
            for clothing_type in rules['required']:
                items = suitable_clothing.get(clothing_type, [])
                if items:
                    # 随机选择，但避免重复
                    selected = random.choice(items)
                    outfit['items'][clothing_type] = selected
                else:
                    outfit['missing'].append(CLOTHING_TYPES.get(clothing_type, clothing_type))
            
            # 可选的衣物类型
            for clothing_type in rules.get('optional', []):
                items = suitable_clothing.get(clothing_type, [])
                if items and random.random() > 0.3:  # 70%概率添加可选配件
                    selected = random.choice(items)
                    outfit['items'][clothing_type] = selected
            
            # 计算组合评分
            outfit['score'] = cls._calculate_score(outfit)
            outfit['total_items'] = len(outfit['items'])
            
            recommendations.append(outfit)
        
        # 按评分排序
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations
    
    @staticmethod
    def _calculate_score(outfit):
        """计算穿搭组合评分"""
        score = 0
        items = outfit.get('items', {})
        
        # 基础分：有衣物就有分
        score += len(items) * 20
        
        # 完整度加分：必需项都有
        if not outfit.get('missing'):
            score += 30
        
        # 颜色搭配加分（简单规则）
        colors = [item.get('color') for item in items.values() if item.get('color')]
        if colors:
            # 颜色数量适中（2-3种）加分
            unique_colors = set(colors)
            if 2 <= len(unique_colors) <= 3:
                score += 20
            # 包含黑白灰等百搭色加分
            neutral_colors = {'black', 'white', 'gray', 'beige'}
            if unique_colors & neutral_colors:
                score += 10
        
        return min(score, 100)  # 最高100分
    
    @classmethod
    def get_wardrobe_summary(cls):
        """获取衣橱概况"""
        stats = ClothingModel.get_statistics()
        all_items = ClothingModel.get_all()
        
        # 按温度范围统计
        temp_coverage = {}
        for level, range_info in TEMPERATURE_RANGES.items():
            mid_temp = (range_info['min'] + range_info['max']) / 2
            items = ClothingModel.get_by_temperature(mid_temp)
            temp_coverage[level] = {
                'label': range_info['label'],
                'count': len(items),
                'has_complete_outfit': cls._check_complete_outfit(items)
            }
        
        return {
            'statistics': stats,
            'temperature_coverage': temp_coverage,
            'recent_items': all_items[:5] if all_items else []
        }
    
    @staticmethod
    def _check_complete_outfit(items):
        """检查是否有完整的穿搭组合"""
        types = {item['type'] for item in items}
        required = {'tops', 'bottoms', 'shoes'}
        return required.issubset(types)
