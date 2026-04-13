"""
Vercel 部署入口文件
"""
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

from app import app

# Vercel 使用这个作为 handler
handler = app
