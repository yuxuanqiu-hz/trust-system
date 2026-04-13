"""
信托管理系统 - 数据库模型
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """用户表（管理员 + 普通员工）"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # 登录用户名（手机号）
    phone = db.Column(db.String(50), unique=True, nullable=False, index=True)  # 手机号（登录用）
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
        return check_password_hash(self.password_hash, password)
    @property
    def password_hash(self):
        return self._password_hash or ''
    @password_hash.setter
    def password_hash(self, value):
        self._password_hash = value


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
    
    # 第一次分配
    first_exercise_shares = db.Column(db.Numeric(20, 4))  # 行权数
    first_sold_shares = db.Column(db.Numeric(20, 4))  # 出售数
    first_income = db.Column(db.Numeric(20, 4))  # 交易收入
    first_cost = db.Column(db.Numeric(20, 4))  # 行权成本
    first_fee = db.Column(db.Numeric(20, 4))  # 交易费用
    first_allocated_shares = db.Column(db.Numeric(20, 4))  # 分配股数
    first_cash = db.Column(db.Numeric(20, 4))  # 现金收益
    
    # 第二次分配
    second_exercise_shares = db.Column(db.Numeric(20, 4))  # 行权数
    second_sold_shares = db.Column(db.Numeric(20, 4))  # 出售数
    second_income = db.Column(db.Numeric(20, 4))  # 交易收入
    second_cost = db.Column(db.Numeric(20, 4))  # 成本
    second_fee = db.Column(db.Numeric(20, 4))  # 总交易费用
    second_share_change = db.Column(db.Numeric(20, 4))  # 股数变动值
    second_cash = db.Column(db.Numeric(20, 4))  # 分配现金金额
    
    # 累计
    total_exercise_shares = db.Column(db.Numeric(20, 4))  # 累计行权数
    total_sold_shares = db.Column(db.Numeric(20, 4))  # 累计出售数
    total_income = db.Column(db.Numeric(20, 4))  # 累计交易收入
    total_cost = db.Column(db.Numeric(20, 4))  # 累计行权成本
    total_fee = db.Column(db.Numeric(20, 4))  # 累计交易费用
    remaining_shares = db.Column(db.Numeric(20, 4))  # 累计剩余待分配股票
    total_allocated = db.Column(db.Numeric(20, 4))  # 累计分配金额
    
    # 剩余
    remaining_exercisable = db.Column(db.Numeric(20, 4))  # 剩余可行权股数
    exercisable_sellable = db.Column(db.Numeric(20, 4))  # 行权可卖股数
    sell_income = db.Column(db.Numeric(20, 4))  # 卖股收益
    sell_tax = db.Column(db.Numeric(20, 4))  # 卖股缴税
    total_sell = db.Column(db.Numeric(20, 4))  # 合计卖股
    
    # 问卷信息
    survey_type = db.Column(db.String(100))  # 问卷类型
    is_exercised = db.Column(db.String(50))  # 是否行权
    exercise_qty = db.Column(db.String(50))  # 行权数量
    exercise_price = db.Column(db.String(50))  # 行权价
    is_sold = db.Column(db.String(50))  # 是否卖股
    sold_qty = db.Column(db.String(50))  # 卖出股票数量
    sold_price = db.Column(db.String(50))  # 卖股价格
    sold_tax_flag = db.Column(db.String(50))  # 卖股缴税
    sold_tax_price = db.Column(db.String(50))  # 卖股缴税价格
    
    data_source = db.Column(db.String(20), default='import')
    import_batch = db.Column(db.String(50))  # 导入批次
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id, 'employee_no': self.employee_no, 'name': self.name,
            'grant_shares': str(self.grant_shares) if self.grant_shares else None,
            'vested_shares': str(self.vested_shares) if self.vested_shares else None,
            'vested_ratio': str(self.vested_ratio) if self.vested_ratio else None,
            'total_income': str(self.total_income) if self.total_income else None,
            'total_allocated': str(self.total_allocated) if self.total_allocated else None,
        }
