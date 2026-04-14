# 股票管理系统 - 生产环境配置
import os

class Config:
    # 安全密钥（生产环境请修改）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'trust-system-prod-key-2026-change-this'
    
    # 数据库配置
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(BASE_DIR, "instance/trust.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 会话配置
    PERMANENT_SESSION_LIFETIME = 3600  # 1 小时
    SESSION_COOKIE_SECURE = True  # 仅 HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # 文件上传
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    
    # 验证码
    VERIFY_CODE_LENGTH = 6
    VERIFY_CODE_EXPIRE = 300  # 5 分钟
    
    # 分页
    ITEMS_PER_PAGE = 20
