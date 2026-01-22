#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLite数据库模型
"""
import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager
from config import DATABASE_PATH

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # 返回字典形式的结果
    return conn

@contextmanager
def db_session():
    """数据库会话上下文管理器"""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_database():
    """初始化数据库表"""
    with db_session() as conn:
        cursor = conn.cursor()
        
        # 衣物表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clothing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                color TEXT,
                style TEXT,
                temp_min INTEGER DEFAULT 0,
                temp_max INTEGER DEFAULT 40,
                image_path TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 穿搭组合表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS outfits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                top_id INTEGER,
                bottom_id INTEGER,
                outerwear_id INTEGER,
                shoes_id INTEGER,
                accessories_id INTEGER,
                temp_min INTEGER,
                temp_max INTEGER,
                style TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (top_id) REFERENCES clothing(id),
                FOREIGN KEY (bottom_id) REFERENCES clothing(id),
                FOREIGN KEY (outerwear_id) REFERENCES clothing(id),
                FOREIGN KEY (shoes_id) REFERENCES clothing(id),
                FOREIGN KEY (accessories_id) REFERENCES clothing(id)
            )
        ''')
        
        # 推荐历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL,
                weather TEXT,
                city TEXT,
                outfit_ids TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        print("数据库初始化完成")

class ClothingModel:
    """衣物数据模型"""
    
    @staticmethod
    def add(name, clothing_type, color=None, style=None, temp_min=0, temp_max=40, 
            image_path=None, description=None):
        """添加衣物"""
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO clothing (name, type, color, style, temp_min, temp_max, image_path, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, clothing_type, color, style, temp_min, temp_max, image_path, description))
            return cursor.lastrowid
    
    @staticmethod
    def get_by_id(clothing_id):
        """根据ID获取衣物"""
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM clothing WHERE id = ?', (clothing_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def get_all(clothing_type=None):
        """获取所有衣物，可按类型筛选"""
        with db_session() as conn:
            cursor = conn.cursor()
            if clothing_type:
                cursor.execute('SELECT * FROM clothing WHERE type = ? ORDER BY created_at DESC', 
                             (clothing_type,))
            else:
                cursor.execute('SELECT * FROM clothing ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_by_temperature(temperature, clothing_type=None):
        """根据温度获取适合的衣物"""
        with db_session() as conn:
            cursor = conn.cursor()
            if clothing_type:
                cursor.execute('''
                    SELECT * FROM clothing 
                    WHERE temp_min <= ? AND temp_max >= ? AND type = ?
                    ORDER BY created_at DESC
                ''', (temperature, temperature, clothing_type))
            else:
                cursor.execute('''
                    SELECT * FROM clothing 
                    WHERE temp_min <= ? AND temp_max >= ?
                    ORDER BY type, created_at DESC
                ''', (temperature, temperature))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def update(clothing_id, **kwargs):
        """更新衣物信息"""
        allowed_fields = ['name', 'type', 'color', 'style', 'temp_min', 'temp_max', 
                         'image_path', 'description']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}
        
        if not updates:
            return False
            
        with db_session() as conn:
            cursor = conn.cursor()
            set_clause = ', '.join([f'{k} = ?' for k in updates.keys()])
            values = list(updates.values()) + [clothing_id]
            cursor.execute(f'''
                UPDATE clothing SET {set_clause}, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', values)
            return cursor.rowcount > 0
    
    @staticmethod
    def delete(clothing_id):
        """删除衣物"""
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM clothing WHERE id = ?', (clothing_id,))
            return cursor.rowcount > 0
    
    @staticmethod
    def get_statistics():
        """获取衣橱统计信息"""
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT type, COUNT(*) as count 
                FROM clothing 
                GROUP BY type
            ''')
            type_counts = {row['type']: row['count'] for row in cursor.fetchall()}
            
            cursor.execute('SELECT COUNT(*) as total FROM clothing')
            total = cursor.fetchone()['total']
            
            return {
                'total': total,
                'by_type': type_counts
            }

# 初始化数据库
if __name__ == '__main__':
    init_database()
