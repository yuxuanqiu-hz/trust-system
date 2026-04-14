"""
初始化数据库 - 创建管理员账号
"""
import os
from flask import Flask, jsonify
from models import db, User, get_database_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def init_admin():
    """初始化管理员账号"""
    with app.app_context():
        db.create_all()
        
        # 删除旧管理员
        User.query.filter_by(phone='15382303557').delete()
        User.query.filter_by(phone='15381150723').delete()
        
        # 创建管理员 - 裘宇轩
        admin1 = User(
            username='15382303557',
            phone='15382303557',
            name='裘宇轩',
            employee_no='0000001',  # 工号
            role='admin'
        )
        admin1.set_password('admin123')  # 密码
        db.session.add(admin1)
        
        # 创建管理员 - 舒苗
        admin2 = User(
            username='15381150723',
            phone='15381150723',
            name='舒苗',
            employee_no='0000002',  # 工号
            role='admin'
        )
        admin2.set_password('admin123')  # 密码
        db.session.add(admin2)
        
        db.session.commit()
        
        print("✅ 管理员账号已创建")
        print("裘宇轩 - 手机号：15382303557, 工号：0000001, 密码：admin123")
        print("舒苗 - 手机号：15381150723, 工号：0000002, 密码：admin123")

if __name__ == '__main__':
    init_admin()
