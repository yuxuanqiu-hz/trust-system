"""
批量导入员工账号脚本
"""
import sys
sys.path.insert(0, '/home/admin/openclaw/workspace/trust-system')

from app import app, db
from models import User
import pandas as pd

def import_employees():
    file_path = '/home/admin/共享文件/曹操出行 - 股票全部员工列表 (2).xlsx'
    
    with app.app_context():
        df = pd.read_excel(file_path)
        print(f"读取到 {len(df)} 条员工数据")
        
        created = 0
        updated = 0
        skipped = 0
        
        for _, row in df.iterrows():
            phone = str(row.get('手机号', ''))
            # 清理手机号格式：去掉 +86、空格、横杠
            phone = phone.replace('+86', '').replace(' ', '').replace('-', '').strip()
            
            if len(phone) != 11 or not phone.startswith('1'):
                print(f"跳过无效手机号：{phone} - {row.get('姓名')}")
                skipped += 1
                continue
            
            # 检查是否已存在
            user = User.query.filter_by(phone=phone).first()
            
            if user:
                # 更新现有用户
                user.name = row.get('姓名')
                user.employee_no = str(row.get('工号', ''))
                user.email = row.get('员工邮箱')
                user.department = row.get('标签')
                updated += 1
            else:
                # 创建新用户
                user = User(
                    username=phone,
                    phone=phone,
                    name=row.get('姓名'),
                    employee_no=str(row.get('工号', '')),
                    email=row.get('员工邮箱'),
                    department=row.get('标签'),
                    role='user'
                )
                db.session.add(user)
                created += 1
        
        db.session.commit()
        print(f"\n导入完成!")
        print(f"  新增：{created} 人")
        print(f"  更新：{updated} 人")
        print(f"  跳过：{skipped} 人")
        
        # 创建管理员账号
        admins = [
            {'name': '裘宇轩', 'phone': '15382303557', 'employee_no': 'admin_qyx'},
            {'name': '舒苗', 'phone': '15381150723', 'employee_no': 'admin_sm'}
        ]
        
        for admin_data in admins:
            admin = User.query.filter_by(phone=admin_data['phone']).first()
            if not admin:
                admin = User(
                    username=admin_data['phone'],
                    phone=admin_data['phone'],
                    name=admin_data['name'],
                    employee_no=admin_data['employee_no'],
                    role='admin'
                )
                db.session.add(admin)
                print(f"创建管理员：{admin_data['name']} - {admin_data['phone']}")
            else:
                admin.role = 'admin'
                admin.name = admin_data['name']
                print(f"更新管理员：{admin_data['name']} - {admin_data['phone']}")
        
        db.session.commit()
        print("\n管理员账号创建完成!")

if __name__ == '__main__':
    import_employees()
