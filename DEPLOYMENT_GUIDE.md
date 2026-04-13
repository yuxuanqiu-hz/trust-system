# 信托管理系统 - 部署指南

## 📋 目录

1. [快速部署（推荐）](#快速部署)
2. [生产环境部署](#生产环境部署)
3. [内网穿透方案](#内网穿透方案)
4. [安全配置](#安全配置)
5. [常见问题](#常见问题)

---

## 🚀 快速部署

### 适用场景
- 公司内部测试
- 局域网访问
- 快速验证功能

### 部署步骤

```bash
cd /home/admin/openclaw/workspace/trust-system
bash deploy-quick.sh
```

### 访问方式

**局域网访问：**
```
http://10.1.16.227:5001
```

**本机访问：**
```
http://localhost:5001
```

### 管理员账号
- 裘宇轩 - 15382303557
- 舒苗 - 15381150723

---

## 🏢 生产环境部署

### 适用场景
- 正式使用
- 多用户访问
- 需要 HTTPS

### 前置要求

1. **域名**（可选，可用 IP 代替）
2. **服务器**（推荐配置：2 核 4G 以上）
3. **sudo 权限**

### 部署步骤

```bash
# 1. 进入目录
cd /home/admin/openclaw/workspace/trust-system

# 2. 执行生产部署（需要 sudo）
sudo bash deploy-prod.sh

# 3. 按提示完成 SSL 证书配置
```

### 访问方式

**HTTPS 访问：**
```
https://your-domain.com
或
https://你的公网 IP
```

### 服务管理

```bash
# 查看状态
systemctl status trust-system

# 重启服务
systemctl restart trust-system

# 查看日志
journalctl -u trust-system -f

# 停止服务
systemctl stop trust-system
```

---

## 🌐 内网穿透方案

### 方案 1：Ngrok（推荐）

```bash
# 1. 下载 ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xzf ngrok-v3-stable-linux-amd64.tgz

# 2. 启动 ngrok
./ngrok http 5001

# 3. 获取公网访问地址
# ngrok 会显示一个 https://xxx.ngrok.io 的地址
```

### 方案 2：FRP

```bash
# 1. 配置 frpc.ini
[common]
server_addr = your-server-ip
server_port = 7000

[trust-system]
type = tcp
local_ip = 127.0.0.1
local_port = 5001
remote_port = 6000

# 2. 启动 frpc
./frpc -c frpc.ini

# 3. 访问
# http://your-server-ip:6000
```

### 方案 3：Cloudflare Tunnel

```bash
# 1. 安装 cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64

# 2. 启动 tunnel
./cloudflared-linux-amd64 tunnel --url http://localhost:5001

# 3. 获取访问地址
```

---

## 🔒 安全配置

### 1. 修改密钥

编辑 `prod_config.py`：
```python
SECRET_KEY = 'your-unique-secret-key-here'
```

### 2. 配置防火墙

```bash
# 使用 UFW
sudo ufw allow 5001/tcp
sudo ufw enable

# 或使用 iptables
sudo iptables -A INPUT -p tcp --dport 5001 -j ACCEPT
```

### 3. 限制访问 IP

编辑 `nginx.conf`：
```nginx
location / {
    allow 192.168.1.0/24;  # 只允许公司内网
    deny all;
    proxy_pass http://127.0.0.1:5001;
    ...
}
```

### 4. 接入短信服务

当前验证码显示在日志中，生产环境建议接入：
- 阿里云短信
- 腾讯云短信
-  twilio（国际）

---

## ❓ 常见问题

### Q1: 无法访问 5001 端口

**解决：**
```bash
# 检查服务是否运行
ps aux | grep "python3 app.py"

# 检查防火墙
sudo ufw status
sudo ufw allow 5001/tcp

# 检查端口占用
netstat -tlnp | grep 5001
```

### Q2: 浏览器显示"连接被拒绝"

**解决：**
1. 确认服务已启动
2. 检查防火墙设置
3. 确认 IP 地址正确

### Q3: 如何备份数据

```bash
# 备份数据库
cp /home/admin/openclaw/workspace/trust-system/instance/trust.db \
   /backup/trust-db-$(date +%Y%m%d).db

# 恢复数据库
cp /backup/trust-db-20260412.db \
   /home/admin/openclaw/workspace/trust-system/instance/trust.db
```

### Q4: 如何添加新用户

方法 1：通过管理界面导入 Excel
方法 2：直接添加到数据库

```python
# 使用 Python 脚本
cd /home/admin/openclaw/workspace/trust-system
python3 << 'EOF'
from app import app, db
from models import User

with app.app_context():
    user = User(
        username='13800138000',
        phone='13800138000',
        name='张三',
        employee_no='0000001',
        role='user'
    )
    db.session.add(user)
    db.session.commit()
    print('用户添加成功')
EOF
```

---

## 📞 技术支持

**系统目录：** `/home/admin/openclaw/workspace/trust-system/`

**日志文件：**
- 应用日志：`/tmp/trust-app.log`
- 系统日志：`journalctl -u trust-system`
- Nginx 日志：`/var/log/nginx/`

**配置文件：**
- Nginx：`/etc/nginx/sites-available/trust-system`
- Systemd：`/etc/systemd/system/trust-system.service`

---

**最后更新：** 2026-04-13
**版本：** v2.0
