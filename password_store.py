"""
全局密码存储
"""
# 存储用户 ID 到明文密码的映射
USER_PASSWORDS = {}

def set_user_password(user_id, password):
    """保存用户密码"""
    USER_PASSWORDS[user_id] = password
    print(f"[密码存储] 用户 {user_id} 密码已保存：{password}")

def get_user_password(user_id):
    """获取用户密码"""
    return USER_PASSWORDS.get(user_id, 'admin123')

def load_passwords_from_db():
    """从数据库加载所有密码"""
    from app import app, db
    from models import User
    
    with app.app_context():
        users = User.query.all()
        for user in users:
            if hasattr(user, '_plain_pwd') and user._plain_pwd:
                USER_PASSWORDS[user.id] = user._plain_pwd
                print(f"[密码加载] 用户 {user.id} ({user.name}) 密码：{user._plain_pwd}")
