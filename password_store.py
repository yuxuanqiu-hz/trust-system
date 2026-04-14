"""
全局密码存储（简化版）
"""
# 存储用户 ID 到明文密码的映射
USER_PASSWORDS = {}

def set_user_password(user_id, password):
    """保存用户密码"""
    USER_PASSWORDS[user_id] = password

def get_user_password(user_id):
    """获取用户密码"""
    return USER_PASSWORDS.get(user_id, 'admin123')

def load_passwords_from_db():
    """从数据库加载所有密码（在应用启动时调用）"""
    # 这个函数在 app.py 中调用，延迟导入避免循环依赖
    pass
