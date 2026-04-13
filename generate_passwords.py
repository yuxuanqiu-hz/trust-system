#!/usr/bin/env python3
"""
为所有用户生成随机密码并导出 Excel
"""
import sys
sys.path.insert(0, '/home/admin/openclaw/workspace/trust-system')

from app import app, db
from models import User
import pandas as pd
import random
import string
from datetime import datetime

def generate_password(length=10):
    """生成随机密码"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

with app.app_context():
    # 获取所有用户
    users = User.query.all()
    
    # 生成密码
    password_list = []
    for user in users:
        password = generate_password()
        user.set_password(password)
        password_list.append({
            '姓名': user.name,
            '手机号': user.phone,
            '工号': user.employee_no,
            '角色': '管理员' if user.role == 'admin' else '员工',
            '初始密码': password,
            '备注': '首次登录后请修改密码'
        })
        print(f"{user.name} ({user.phone}): {password}")
    
    db.session.commit()
    
    # 导出 Excel
    df = pd.DataFrame(password_list)
    filename = f'/home/admin/openclaw/workspace/trust-system/账号密码表_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    df.to_excel(filename, index=False)
    
    print(f"\n✅ 已生成 {len(users)} 个账号密码")
    print(f"📁 Excel 文件：{filename}")
    print("\n⚠️  重要提示：")
    print("1. 请将此 Excel 文件分发给对应员工")
    print("2. 建议首次登录后强制修改密码")
    print("3. 妥善保管此文件，不要泄露")
