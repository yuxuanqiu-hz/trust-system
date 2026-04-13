"""
初始化数据库脚本 - 创建管理员账号和导入初始数据
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, User, TrustData, get_database_url
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_admin():
    """创建管理员账号"""
    database_url = get_database_url()
    print(f"连接数据库：{database_url[:50]}...")
    
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 检查是否已有管理员
    admin = session.query(User).filter_by(phone='15382303557').first()
    
    if admin:
        print("✅ 管理员账号已存在")
    else:
        admin = User(
            username='15382303557',
            phone='15382303557',
            name='裘宇轩',
            employee_no='admin',
            role='admin'
        )
        admin.password_hash = generate_password_hash('V^!y3#Ip2i')
        session.add(admin)
        session.commit()
        print("✅ 管理员账号已创建")
    
    # 创建第二个管理员
    admin2 = session.query(User).filter_by(phone='15381150723').first()
    if not admin2:
        admin2 = User(
            username='15381150723',
            phone='15381150723',
            name='舒苗',
            employee_no='admin_sm',
            role='admin'
        )
        admin2.password_hash = generate_password_hash('eDCRD4QzmG')
        session.add(admin2)
        session.commit()
        print("✅ 舒苗账号已创建")
    
    # 统计
    user_count = session.query(User).count()
    print(f"📊 总用户数：{user_count}")
    
    session.close()
    print("✅ 初始化完成")

if __name__ == '__main__':
    init_admin()
