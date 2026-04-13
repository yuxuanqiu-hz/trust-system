#!/bin/bash
# 信托管理系统 - 生产环境部署脚本

set -e

echo "============================================================"
echo "信托管理系统 - 生产环境部署"
echo "============================================================"

# 1. 检查权限
if [ "$EUID" -ne 0 ]; then 
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

# 2. 安装依赖
echo ""
echo "[1/6] 安装系统依赖..."
apt update
apt install -y nginx python3-pip python3-venv certbot

# 3. 安装 Python 依赖
echo ""
echo "[2/6] 安装 Python 依赖..."
cd /home/admin/openclaw/workspace/trust-system
pip3 install -r requirements.txt
pip3 install gunicorn  # 生产环境 WSGI 服务器

# 4. 配置 systemd 服务
echo ""
echo "[3/6] 配置 systemd 服务..."
cp trust-system.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable trust-system
systemctl start trust-system

# 5. 配置 Nginx
echo ""
echo "[4/6] 配置 Nginx..."
mkdir -p /etc/nginx/ssl
cp nginx.conf /etc/nginx/sites-available/trust-system
ln -sf /etc/nginx/sites-available/trust-system /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 6. 生成 SSL 证书（自签名，生产环境建议使用 Let's Encrypt）
echo ""
echo "[5/6] 生成 SSL 证书..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/trust.key \
    -out /etc/nginx/ssl/trust.crt \
    -subj "/C=CN/ST=State/L=City/O=Company/CN=trust"

# 7. 启动服务
echo ""
echo "[6/6] 启动服务..."
systemctl restart nginx
systemctl status trust-system --no-pager
systemctl status nginx --no-pager

echo ""
echo "============================================================"
echo "✅ 部署完成！"
echo "============================================================"
echo ""
echo "访问地址：https://$(hostname -I | awk '{print $1}')"
echo ""
echo "管理员账号："
echo "  裘宇轩 - 15382303557"
echo "  舒苗 - 15381150723"
echo ""
echo "管理命令："
echo "  查看状态：systemctl status trust-system"
echo "  重启服务：systemctl restart trust-system"
echo "  查看日志：journalctl -u trust-system -f"
echo "  停止服务：systemctl stop trust-system"
echo ""
echo "⚠️  注意："
echo "  1. 当前使用自签名证书，浏览器会显示安全警告"
echo "  2. 生产环境建议使用 Let's Encrypt 免费证书"
echo "  3. 请修改 prod_config.py 中的 SECRET_KEY"
echo "============================================================"
