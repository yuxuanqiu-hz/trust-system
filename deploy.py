#!/usr/bin/env python3
"""
股票管理系统 - 完整部署脚本
"""
import sys, os, glob
sys.path.insert(0, '/home/admin/openclaw/workspace/trust-system')
os.chdir('/tmp')

from app import app, db
from models import User, TrustData
import pandas as pd

def deploy():
    print("=" * 60)
    print("股票管理系统 - 完整部署")
    print("=" * 60)
    
    with app.app_context():
        # 1. 重建数据库
        print("\n[1/4] 重建数据库...")
        db.drop_all()
        db.create_all()
        print("  ✓ 数据库已创建")
        
        # 2. 创建管理员账号
        print("\n[2/4] 创建管理员账号...")
        admin_qiu = User(
            username='15382303557',
            phone='15382303557',
            name='裘宇轩',
            employee_no='admin',
            role='admin'
        )
        db.session.add(admin_qiu)
        
        admin_shu = User(
            username='15381150723',
            phone='15381150723',
            name='舒苗',
            employee_no='099818',
            role='admin'
        )
        db.session.add(admin_shu)
        db.session.commit()
        print("  ✓ 管理员：裘宇轩 (15382303557)")
        print("  ✓ 管理员：舒苗 (15381150723)")
        
        # 3. 导入员工账号（35 人，排除舒苗）
        print("\n[3/4] 导入员工账号...")
        files = glob.glob('*员工*.xlsx')
        if not files:
            print("  ✗ 未找到员工清单文件")
            return False
        
        df_emp = pd.read_excel(files[0])
        employee_count = 0
        
        for _, row in df_emp.iterrows():
            phone_raw = str(row.get('手机号', ''))
            # 标准化手机号格式（去掉 +86 和空格）
            phone = phone_raw.replace('+86', '').replace(' ', '').replace('-', '').strip()
            
            # 跳过舒苗
            if phone == '15381150723':
                continue
            
            if phone == 'nan' or not phone or len(phone) < 10:
                continue
            
            emp_no_raw = row.get('工号')
            try:
                emp_no = str(int(emp_no_raw)).zfill(7) if pd.notna(emp_no_raw) else ''
            except:
                emp_no = ''
            
            name = str(row.get('姓名', ''))
            email = str(row.get('员工邮箱', '')) if pd.notna(row.get('员工邮箱')) else None
            
            user = User(
                username=phone,
                phone=phone,
                name=name,
                employee_no=emp_no,
                email=email,
                role='user'
            )
            db.session.add(user)
            employee_count += 1
        
        db.session.commit()
        print(f"  ✓ 导入员工：{employee_count} 人")
        
        # 4. 导入股票数据
        print("\n[4/4] 导入股票数据...")
        df_trust = pd.read_excel('/home/admin/共享文件/自建股票系统数据.xlsx')
        trust_count = 0
        
        for _, row in df_trust.iterrows():
            emp_no_raw = row.get('工号')
            if pd.isna(emp_no_raw):
                continue
            try:
                emp_no = str(int(emp_no_raw)).zfill(7)
            except:
                continue
            
            record = TrustData(employee_no=emp_no)
            record.name = str(row.get('姓名', '')) if pd.notna(row.get('姓名')) else None
            record.grant_shares = row.get('授予数') if pd.notna(row.get('授予数')) else None
            record.valid_vested = row.get('有效已归属') if pd.notna(row.get('有效已归属')) else None
            record.exercised_shares = row.get('累计已行权') if pd.notna(row.get('累计已行权')) else None
            record.sold_shares = row.get('累计已出售') if pd.notna(row.get('累计已出售')) else None
            record.remaining_exercisable = row.get('剩余可行权') if pd.notna(row.get('剩余可行权')) else None
            record.remaining_sellable = row.get('剩余可出售') if pd.notna(row.get('剩余可出售')) else None
            record.allocated_cash = row.get('已分配现金（HKD）') if pd.notna(row.get('已分配现金（HKD）')) else None
            record.lock_period = str(row.get('锁定期')) if pd.notna(row.get('锁定期')) else None
            db.session.add(record)
            trust_count += 1
        
        db.session.commit()
        print(f"  ✓ 导入股票数据：{trust_count} 条")
        
        # 5. 统计
        print("\n" + "=" * 60)
        print("部署完成！")
        print("=" * 60)
        print(f"总账号数：{User.query.count()}")
        print(f"  - 管理员：{User.query.filter_by(role='admin').count()} 人")
        print(f"  - 员工：{User.query.filter_by(role='user').count()} 人")
        print(f"股票数据：{TrustData.query.count()} 条")
        print("\n访问地址：http://10.1.16.227:5001")
        print("\n管理员账号：")
        print("  裘宇轩 - 15382303557")
        print("  舒苗 - 15381150723")
        print("=" * 60)
        
        return True

if __name__ == '__main__':
    success = deploy()
    sys.exit(0 if success else 1)
