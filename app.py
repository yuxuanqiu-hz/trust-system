"""
信托管理系统 - 主应用
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, TrustData, get_database_url
from datetime import datetime, timedelta
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'trust-system-secret-key-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 初始化数据库
def init_db():
    with app.app_context():
        db.create_all()
        # 如果没有任何用户，创建管理员账号
        if not User.query.first():
            admin = User(username='15382303557', phone='15382303557', name='裘宇轩', employee_no='admin', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('✅ 管理员账号已创建')

init_db()

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

# ============ 用户管理 ============

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
                User.phone.contains(search),
                User.employee_no.contains(search)
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

# ============ 数据管理 ============

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

# ============ 数据导入 ============

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
                    import pandas as pd
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
                        
                        # 字段映射（支持多种列名格式）
                        record.name = str(row.get('姓名') or row.get('Name') or '') if pd.notna(row.get('姓名') or row.get('Name')) else None
                        
                        # 授予数
                        grant_val = row.get('授予数') or row.get('授予数（股）') or row.get('Grant Shares') or 0
                        record.grant_shares = grant_val if pd.notna(grant_val) else None
                        
                        # 有效已归属
                        vested_val = row.get('有效已归属') or row.get('已归属') or row.get('Vested Shares') or 0
                        record.valid_vested = vested_val if pd.notna(vested_val) else None
                        
                        # 累计已行权
                        exercised_val = row.get('累计已行权股数') or row.get('累计行权数') or row.get('Exercised Shares') or 0
                        record.exercised_shares = exercised_val if pd.notna(exercised_val) else None
                        
                        # 累计已出售
                        sold_val = row.get('累计已出售股数') or row.get('累计出售数') or row.get('Sold Shares') or 0
                        record.sold_shares = sold_val if pd.notna(sold_val) else None
                        
                        # 剩余可行权
                        rem_exer_val = row.get('剩余可行权股数') or row.get('剩余可行权') or row.get('Remaining Exercisable') or 0
                        record.remaining_exercisable = rem_exer_val if pd.notna(rem_exer_val) else None
                        
                        # 剩余可出售
                        rem_sell_val = row.get('剩余可出售股数') or row.get('行权可卖股数') or row.get('Remaining Sellable') or 0
                        record.remaining_sellable = rem_sell_val if pd.notna(rem_sell_val) else None
                        
                        # 已分配现金
                        cash_val = row.get('已分配现金额（HKD）') or row.get('累计分配金额') or row.get('Allocated Cash') or 0
                        record.allocated_cash = cash_val if pd.notna(cash_val) else None
                        record.lock_period = str(row.get('锁定期')) if pd.notna(row.get('锁定期')) else None
                        count += 1
                    
                    db.session.commit()
                    flash(f'✓ 成功导入信托数据 {count} 条，跳过 {skipped} 条', 'success')
                
                elif import_type == 'employees':
                    # 导入员工账号
                    import pandas as pd
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
                if os.path.exists(filepath):
                    os.remove(filepath)
            
            return redirect(url_for('admin_import'))
    
    return render_template('import.html', trust_count=trust_count, user_count=user_count, 
                         admin_count=admin_count, batch_name=batch_name)

# ============ 修改密码 ============

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(old_password):
            flash('原密码错误', 'danger')
            return render_template('change_password.html')
        
        if len(new_password) < 6:
            flash('密码长度至少 6 位', 'danger')
            return render_template('change_password.html')
        
        if new_password != confirm_password:
            flash('两次输入的密码不一致', 'danger')
            return render_template('change_password.html')
        
        current_user.set_password(new_password)
        db.session.commit()
        flash('✓ 密码修改成功', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('change_password.html')

# ============ 初始化 API ============

@app.route('/api/init')
def init_data():
    """初始化管理员账号"""
    with app.app_context():
        db.create_all()
        
        # 删除旧管理员
        User.query.filter_by(phone='15382303557').delete()
        User.query.filter_by(phone='15381150723').delete()
        
        # 创建新管理员 - 裘宇轩
        admin = User(username='15382303557', phone='15382303557', name='裘宇轩', 
                    employee_no='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # 创建第二个管理员 - 舒苗
        admin2 = User(username='15381150723', phone='15381150723', name='舒苗', 
                     employee_no='admin_sm', role='admin')
        admin2.set_password('admin123')
        db.session.add(admin2)
        
        db.session.commit()
        return jsonify({
            'status': 'success', 
            'message': '管理员账号已创建',
            'account1': '15382303557 / admin123',
            'account2': '15381150723 / admin123'
        })

# Vercel 部署入口
handler = app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
