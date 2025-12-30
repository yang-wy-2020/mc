import os

# 上传配置
class UploadConfig:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 上传相关配置
    UPLOAD_FOLDER = 'static/uploads'  # 上传文件保存目录
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 最大文件大小（5MB）
    
    # 自定义选项
    ALLOWED_EXTENSIONS = {
        'images': {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'},
        'documents': {'pdf', 'doc', 'docx', 'txt'},
        'archives': {'zip', 'rar', '7z'}
    }
    
    # 上传选项
    UPLOAD_OPTIONS = {
        'allow_multiple': True,      # 是否允许多文件上传
        'auto_rename': True,         # 自动重命名重复文件
        'create_thumbnail': False,   # 是否创建缩略图
        'thumbnail_size': (200, 200), # 缩略图尺寸
        'watermark': False,          # 是否添加水印
        'watermark_text': '',        # 水印文字
        'compress_images': False,    # 是否压缩图片
        'max_width': 1920,           # 图片最大宽度
    }
    
    # 界面选项
    UI_OPTIONS = {
        'theme': 'light',            # light, dark
        'show_preview': True,        # 是否显示预览
        'drag_drop': True,           # 是否启用拖拽上传
        'show_progress': True,       # 是否显示进度条
        'language': 'zh',            # 界面语言
    }