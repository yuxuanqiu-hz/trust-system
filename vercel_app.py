"""
Vercel 部署入口文件
"""
from app import app

# Vercel 使用这个作为入口
handler = app
