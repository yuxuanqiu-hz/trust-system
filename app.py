"""
信托管理系统 - 主应用
支持手机号 + 验证码登录
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, TrustData
from datetime import datetime, timedelta
import pandas as pd
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'trust-system-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trust.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============ 认证路由 ============

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone', '').replace('+86', '').replace(' ', '').replace('-', '')
        password = request.form.get('password')
        
        user = User.query.filter_by(phone=phone).first()
        
        if not user:
            flash('该手机号未注册', 'danger')
            return render_template('login.html')
        
        if user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('密码错误', 'danger')
    
    return render_template('login.html')

@app.route('/send-code', methods=['POST'])
def send_code():
    """发送验证码"""
    phone = request.form.get('phone', '').replace('+86', '').replace(' ', '').replace('-', '')
    
    if len(phone) != 11 or not phone.startswith('1'):
        return jsonify({'success': False, 'message': '手机号格式不正确'})
    
    user = User.query.filter_by(phone=phone).first()
    if not user:
        return jsonify({'success': False, 'message': '该手机号未注册'})
    
    # 生成 6 位验证码
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    user.verify_code = code
    user.verify_code_expires = datetime.utcnow() + timedelta(minutes=5)
    db.session.commit()
    
    # 实际生产中这里应该发送短信，现在只在日志中打印
    print(f"验证码已生成 - 手机号：{phone}, 验证码：{code}")
    
    return jsonify({
        'success': True,
        'message': f'验证码已生成（测试环境）：{code}',
        'code': code  # 测试环境直接返回验证码
    })

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ============ 仪表盘 ============

@app.route('/')
@login_required
def dashboard():
    if current_user.role == 'admin':
        total_users = User.query.count()
        total_records = TrustData.query.count()
        total_grant_shares = db.session.query(db.func.sum(TrustData.grant_shares)).scalar() or 0
        total_valid_vested = db.session.query(db.func.sum(TrustData.valid_vested)).scalar() or 0
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        return render_template('dashboard.html', 
                             total_users=total_users,
                             total_records=total_records,
                             total_grant_shares=total_grant_shares,
                             total_valid_vested=total_valid_vested,
                             recent_users=recent_users)
    else:
        record = TrustData.query.filter_by(employee_no=current_user.employee_no).first()
        return render_template('employee_dashboard.html', record=record)

# ============ 管理员 - 用户管理 ============

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('无权限访问', 'danger')
        return redirect(url_for('dashboard'))
    
    search = request.args.get('search', '')
    query = User.query
    if search:
        query = query.filter(
            db.or_(
                User.name.contains(search),
                User.employee_no.contains(search),
                User.phone.contains(search)
            )
        )
    users = query.order_by(User.created_at.desc()).all()
    return render_template('users.html', users=users, search=search)

@app.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
def admin_user_add():
    if current_user.role != 'admin':
        flash('无权限访问', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        user = User(
            username=request.form.get('username'),
            phone=request.form.get('phone'),
            employee_no=request.form.get('employee_no'),
            name=request.form.get('name'),
            role=request.form.get('role', 'user'),
            department=request.form.get('department')
        )
        user.set_password(request.form.get('password', '123456'))
        db.session.add(user)
        db.session.commit()
        flash('用户添加成功', 'success')
        return redirect(url_for('admin_users'))
    return render_template('user_form.html', user=None)

# ============ 管理员 - 数据管理 ============

@app.route('/admin/data')
@login_required
def admin_data():
    if current_user.role != 'admin':
        flash('无权限访问', 'danger')
        return redirect(url_for('dashboard'))
    
    search = request.args.get('search', '')
    query = TrustData.query
    if search:
        query = query.filter(
            db.or_(
                TrustData.name.contains(search),
                TrustData.employee_no.contains(search)
            )
        )
    data = query.order_by(TrustData.employee_no).all()
    
    # 计算统计数据
    total_grant = sum(float(r.grant_shares) for r in data if r.grant_shares)
    total_vested = sum(float(r.valid_vested) for r in data if r.valid_vested)
    total_exercised = sum(float(r.exercised_shares) for r in data if r.exercised_shares)
    total_sold = sum(float(r.sold_shares) for r in data if r.sold_shares)
    total_cash = sum(float(r.allocated_cash) for r in data if r.allocated_cash)
    
    return render_template('data.html', data=data, search=search,
                         total_grant=total_grant, total_vested=total_vested,
                         total_exercised=total_exercised, total_sold=total_sold,
                         total_cash=total_cash)

@app.route('/admin/import', methods=['GET', 'POST'])
@login_required
def admin_import():
    if current_user.role != 'admin':
        flash('无权限访问', 'danger')
        return redirect(url_for('dashboard'))
    
    # 获取当前统计
    trust_count = TrustData.query.count()
    user_count = User.query.filter_by(role='user').count()
    admin_count = User.query.filter_by(role='admin').count()
    batch_name = datetime.now().strftime('%Y%m%d')
    
    if request.method == 'POST':
        import_type = request.form.get('import_type', 'trust')
        file = request.files.get('file')
        batch_name = request.form.get('batch_name', datetime.now().strftime('%Y%m%d'))
        
        if file and file.filename.endswith('.xlsx'):
            filepath = f'/tmp/{file.filename}'
            file.save(filepath)
            
            try:
                if import_type == 'trust':
                    # 导入信托数据
                    df = pd.read_excel(filepath)
                    count = 0
                    skipped = 0
                    for _, row in df.iterrows():
                        emp_no_raw = row.get('工号')
                        if pd.isna(emp_no_raw):
                            skipped += 1
                            continue
                        try:
                            emp_no = str(int(emp_no_raw)).zfill(7)
                        except:
                            skipped += 1
                            continue
                        
                        record = TrustData.query.filter_by(employee_no=emp_no).first()
                        if not record:
                            record = TrustData(employee_no=emp_no)
                            db.session.add(record)
                        
                        record.name = str(row.get('姓名', '')) if pd.notna(row.get('姓名')) else None
                        record.grant_shares = row.get('授予数') if pd.notna(row.get('授予数')) else None
                        record.valid_vested = row.get('已归属') if pd.notna(row.get('已归属')) else None
                        record.exercised_shares = row.get('累计行权数') if pd.notna(row.get('累计行权数')) else None
                        record.sold_shares = row.get('累计出售数') if pd.notna(row.get('累计出售数')) else None
                        record.remaining_exercisable = row.get('剩余可行权股数') if pd.notna(row.get('剩余可行权股数')) else None
                        record.remaining_sellable = row.get('行权可卖股数') if pd.notna(row.get('行权可卖股数')) else None
                        record.allocated_cash = row.get('累计分配金额') if pd.notna(row.get('累计分配金额')) else None
                        record.lock_period = str(row.get('锁定期')) if pd.notna(row.get('锁定期')) else None
                        record.import_batch = batch_name
                        count += 1
                    
                    db.session.commit()
                    flash(f'✓ 成功导入信托数据 {count} 条，跳过 {skipped} 条', 'success')
                
                elif import_type == 'employees':
                    # 导入员工账号
                    df = pd.read_excel(filepath)
                    count = 0
                    for _, row in df.iterrows():
                        phone = str(row.get('手机号', '')).replace('+86', '').replace(' ', '').strip()
                        if len(phone) != 11:
                            continue
                        
                        emp_no_raw = row.get('工号')
                        try:
                            emp_no = str(int(emp_no_raw)).zfill(7) if pd.notna(emp_no_raw) else ''
                        except:
                            emp_no = ''
                        
                        name = str(row.get('姓名', ''))
                        email = str(row.get('员工邮箱', '')) if pd.notna(row.get('员工邮箱')) else None
                        
                        if not User.query.filter_by(phone=phone).first():
                            user = User(username=phone, phone=phone, name=name, employee_no=emp_no, email=email, role='user')
                            db.session.add(user)
                            count += 1
                    
                    db.session.commit()
                    flash(f'✓ 成功导入员工账号 {count} 人', 'success')
            
            except Exception as e:
                flash(f'导入失败：{str(e)}', 'danger')
            finally:
                os.remove(filepath)
            
            return redirect(url_for('admin_import'))
    
    return render_template('import.html', trust_count=trust_count, user_count=user_count, 
                         admin_count=admin_count, batch_name=batch_name)
    
    return render_template('import.html')

# ============ 初始化 ============

def init_db():
    with app.app_context():
        db.create_all()
        print('数据库初始化完成')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)
