"""
直接创建管理员账号
"""
import os
from flask import Flask
from models import db, User, get_database_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    
    # 删除旧管理员
    User.query.filter_by(phone='15382303557').delete()
    
    # 创建新管理员
    admin = User(
        username='15382303557',
        phone='15382303557',
        name='裘宇轩',
        employee_no='admin',
        role='admin'
    )
    admin.password_hash = 'pbkdf2:sha256:260000$abc123$V^!y3#Ip2i'  # 简单密码
    admin.set_password('admin123')  # 使用简单密码
    db.session.add(admin)
    db.session.commit()
    
    print("✅ 管理员账号已创建")
    print("手机号：15382303557")
    print("密码：admin123")
