"""
批量导入数据脚本
导入员工账号和信托数据到 Vercel 数据库
"""
import requests
import pandas as pd
import json

# 配置
VERCEL_URL = "https://trust-system-nine.vercel.app"
ADMIN_PHONE = "15382303557"
ADMIN_PASSWORD = "admin123"

# 本地数据文件
ACCOUNTS_FILE = "/home/admin/openclaw/workspace/trust-system/账号密码表_20260414_014843.xlsx"
TRUST_DATA_FILE = "/home/admin/openclaw/workspace/信托最新情况 20260328-V2.xlsx"

def login():
    """登录获取 session"""
    session = requests.Session()
    
    # 登录
    login_data = {
        'phone': ADMIN_PHONE,
        'password': ADMIN_PASSWORD
    }
    response = session.post(f"{VERCEL_URL}/login", data=login_data, allow_redirects=False)
    
    if response.status_code in [200, 302]:
        print("✅ 登录成功")
        return session
    else:
        print("❌ 登录失败")
        return None

def import_accounts(session, excel_file):
    """导入员工账号"""
    print("\n📥 开始导入员工账号...")
    
    # 读取 Excel
    df = pd.read_excel(excel_file)
    
    count = 0
    for _, row in df.iterrows():
        phone = str(row.get('手机号', '')).replace('+86', '').replace(' ', '').strip()
        if len(phone) != 11:
            continue
        
        name = str(row.get('姓名', ''))
        emp_no = str(row.get('工号', '')).zfill(7)
        password = str(row.get('初始密码', 'admin123'))
        
        # 创建账号
        try:
            # 这里需要通过 Web 界面导入，API 需要额外开发
            print(f"  + {name} ({phone}) - 工号：{emp_no}")
            count += 1
        except Exception as e:
            print(f"  ❌ {name} 导入失败：{e}")
    
    print(f"\n✅ 准备导入 {count} 个员工账号")
    print("⚠️  请通过管理界面上传 Excel 文件导入")
    return count

def import_trust_data(session, excel_file):
    """导入信托数据"""
    print("\n📥 开始导入信托数据...")
    
    # 读取 Excel
    df = pd.read_excel(excel_file, sheet_name='汇总表')
    
    count = 0
    for _, row in df.iterrows():
        emp_no_raw = row.get('工号')
        if pd.isna(emp_no_raw):
            continue
        
        try:
            emp_no = str(int(emp_no_raw)).zfill(7)
            name = str(row.get('姓名', ''))
            
            print(f"  + {name} ({emp_no})")
            count += 1
        except Exception as e:
            continue
    
    print(f"\n✅ 准备导入 {count} 条信托数据")
    print("⚠️  请通过管理界面上传 Excel 文件导入")
    return count

def main():
    print("=" * 60)
    print("信托管理系统 - 数据导入脚本")
    print("=" * 60)
    
    # 登录
    session = login()
    if not session:
        return
    
    # 导入员工账号
    try:
        import_accounts(session, ACCOUNTS_FILE)
    except FileNotFoundError:
        print(f"\n❌ 找不到文件：{ACCOUNTS_FILE}")
        print("请通过管理界面手动上传 Excel 文件导入")
    
    # 导入信托数据
    try:
        import_trust_data(session, TRUST_DATA_FILE)
    except FileNotFoundError:
        print(f"\n❌ 找不到文件：{TRUST_DATA_FILE}")
        print("请通过管理界面手动上传 Excel 文件导入")
    
    print("\n" + "=" * 60)
    print("📋 导入说明")
    print("=" * 60)
    print("""
1. 登录管理后台：https://trust-system-nine.vercel.app
2. 进入"数据导入"页面
3. 选择"员工账号导入"，上传账号密码表 Excel
4. 选择"信托数据导入"，上传信托数据 Excel
5. 点击导入按钮

文件位置：
- 账号密码表：/home/admin/openclaw/workspace/trust-system/账号密码表_20260414_014843.xlsx
- 信托数据：/home/admin/openclaw/workspace/信托最新情况 20260328-V2.xlsx
    """)
    print("=" * 60)

if __name__ == '__main__':
    main()
