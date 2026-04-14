"""
数据库迁移脚本 - 创建初始管理员
"""
import sys
sys.path.insert(0, '/home/admin/openclaw/workspace/trust-system')

from app import app, db
from models import User

def create_admin():
    with app.app_context():
        # 检查是否已有管理员
        admin = User.query.filter_by(phone='15382303557').first()
        if admin:
            print('✅ 管理员账号已存在')
            return
        
        # 创建管理员
        admin = User(
            username='15382303557',
            phone='15382303557',
            name='裘宇轩',
            employee_no='admin',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('✅ 管理员账号已创建')
        print('手机号：15382303557')
        print('密码：admin123')

if __name__ == '__main__':
    create_admin()
