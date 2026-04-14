#!/bin/bash
# Railway 部署后初始化脚本

echo "=== 初始化管理员账号 ==="
python3 create_admin.py

echo ""
echo "=== 部署完成 ==="
echo "访问地址：https://trust-system-production.up.railway.app"
echo "管理员账号："
echo "  手机号：15382303557"
echo "  密码：admin123"
