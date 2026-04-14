"""
全局密码存储
"""
# 存储用户 ID 到明文密码的映射
USER_PASSWORDS = {}

def set_user_password(user_id, password):
    """保存用户密码"""
    USER_PASSWORDS[user_id] = password

def get_user_password(user_id):
    """获取用户密码"""
    return USER_PASSWORDS.get(user_id, 'admin123')
