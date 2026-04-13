#!/usr/bin/env python3
"""
批量导入员工账号脚本
从共享文件夹读取员工列表并创建登录账号
"""
import sys
sys.path.insert(0, '/home/admin/openclaw/workspace/trust-system')

from app import app, db
from models import User

# 员工数据（从 Excel 读取的 36 名员工）
employees = [
    ('张德祥', '13305711410', '136083'),
    ('强琦', '13185052977', '308382'),
    ('瞿聪', '13701655620', '308919'),
    ('刘立群', '13918273410', '305220'),
    ('臧珂', '13186972875', '339666'),
]

with app.app_context():
    created = 0
    for name, phone, emp_no in employees:
        user = User.query.filter_by(phone=phone).first()
        if not user:
            user = User(
                username=phone,
                phone=phone,
                name=name,
                employee_no=emp_no,
                role='user'
            )
            db.session.add(user)
            created += 1
            print(f'✓ 创建：{name} - {phone}')
    
    db.session.commit()
    print(f'\n新增员工账号：{created} 人')
    print(f'总账号数：{User.query.count()}')
