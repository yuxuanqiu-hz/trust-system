"""
信托管理系统 - 数据库模型
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

db = SQLAlchemy()

def get_database_url():
    """获取数据库连接 URL"""
    # Vercel 环境变量
    database_url = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')
    
    if database_url:
        # Vercel 的 URL 格式需要转换
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    
    # 本地开发使用 SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join('sqlite:///', os.path.join(basedir, 'instance/trust.db'))

class User(db.Model):
    """用户表（管理员 + 普通员工）"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # 登录用户名（手机号）
    phone = db.Column(db.String(50), unique=True, nullable=False, index=True)  # 手机号（登录用）
    password_hash = db.Column(db.String(256))  # 密码哈希
    verify_code = db.Column(db.String(6))  # 验证码
    verify_code_expires = db.Column(db.DateTime)  # 验证码过期时间
    employee_no = db.Column(db.String(50), index=True)  # 工号（不唯一，允许管理员同时有员工数据）
    name = db.Column(db.String(100))  # 姓名
    role = db.Column(db.String(20), default='user')  # admin/user
    department = db.Column(db.String(100))  # 部门
    email = db.Column(db.String(200))  # 邮箱
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_id(self):
        return str(self.id)
    @property
    def is_authenticated(self):
        return True
    @property
    def is_anonymous(self):
        return False
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return self.password_hash and check_password_hash(self.password_hash, password)


class TrustData(db.Model):
    """信托数据表"""
    __tablename__ = 'trust_data'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_no = db.Column(db.String(50), nullable=False, index=True)  # 工号
    name = db.Column(db.String(100))  # 姓名
    lock_period = db.Column(db.String(50))  # 锁定期
    grant_shares = db.Column(db.Numeric(20, 4))  # 授予数
    valid_vested = db.Column(db.Numeric(20, 4))  # 有效已归属
    exercised_shares = db.Column(db.Numeric(20, 4))  # 累计已行权股数
    sold_shares = db.Column(db.Numeric(20, 4))  # 累计已出售股数
    remaining_exercisable = db.Column(db.Numeric(20, 4))  # 剩余可行权股数
    remaining_sellable = db.Column(db.Numeric(20, 4))  # 剩余可出售股数
    allocated_cash = db.Column(db.Numeric(20, 4))  # 已分配现金额（HKD）
    
    def to_dict(self):
        return {
            'id': self.id, 'employee_no': self.employee_no, 'name': self.name,
            'grant_shares': str(self.grant_shares) if self.grant_shares else None,
            'valid_vested': str(self.valid_vested) if self.valid_vested else None,
            'exercised_shares': str(self.exercised_shares) if self.exercised_shares else None,
            'sold_shares': str(self.sold_shares) if self.sold_shares else None,
            'remaining_exercisable': str(self.remaining_exercisable) if self.remaining_exercisable else None,
            'remaining_sellable': str(self.remaining_sellable) if self.remaining_sellable else None,
            'allocated_cash': str(self.allocated_cash) if self.allocated_cash else None,
        }
