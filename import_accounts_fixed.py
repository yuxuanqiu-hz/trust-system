"""
批量导入员工账号 - 修复密码问题
"""
import pandas as pd
import sys
sys.path.insert(0, '/home/admin/openclaw/workspace/trust-system')

from app import app, db
from models import User

def import_accounts(excel_file):
    """导入员工账号，使用 Excel 中的初始密码"""
    
    # 读取 Excel
    df = pd.read_excel(excel_file)
    
    print("=== 开始导入员工账号 ===\n")
    
    count = 0
    for _, row in df.iterrows():
        phone = str(row.get('手机号', '')).replace('+86', '').replace(' ', '').strip()
        if len(phone) != 11:
            continue
        
        name = str(row.get('姓名', ''))
        emp_no = str(row.get('工号', '')).zfill(7)
        
        # 获取密码 - 优先使用"初始密码"列，其次使用"密码"列，最后使用默认密码
        password = str(row.get('初始密码') or row.get('密码') or row.get('Password') or 'admin123')
        
        with app.app_context():
            # 检查是否已存在
            user = User.query.filter_by(phone=phone).first()
            
            if user:
                # 更新现有用户
                user.name = name
                user.employee_no = emp_no
                user.set_password(password)  # 更新密码
                print(f"✓ 更新：{name} ({phone}) - 工号：{emp_no}, 密码：{password}")
            else:
                # 创建新用户
                user = User(
                    username=phone,
                    phone=phone,
                    name=name,
                    employee_no=emp_no,
                    role='user'
                )
                user.set_password(password)
                db.session.add(user)
                print(f"✓ 创建：{name} ({phone}) - 工号：{emp_no}, 密码：{password}")
            
            db.session.commit()
            count += 1
    
    print(f"\n=== 导入完成 ===")
    print(f"✅ 共导入 {count} 个员工账号")
    print(f"⚠️  请将密码表分发给对应员工")

if __name__ == '__main__':
    file_path = sys.argv[1] if len(sys.argv) > 1 else '/home/admin/openclaw/workspace/trust-system/账号密码表_20260414_014843.xlsx'
    import_accounts(file_path)
