#!/bin/bash
# 信托管理系统 - 快速启动脚本

cd /home/admin/openclaw/workspace/trust-system

# 停止旧进程
pkill -f "python3 app.py" 2>/dev/null
sleep 1

# 启动服务
echo "正在启动信托管理系统..."
nohup python3 app.py > /tmp/trust-app.log 2>&1 &

# 等待启动
sleep 3

# 检查状态
if curl -s http://localhost:5001/login > /dev/null 2>&1; then
    echo "✅ 系统启动成功！"
    echo ""
    echo "访问地址：http://10.1.16.227:5001"
    echo ""
    echo "管理员账号："
    echo "  裘宇轩 - 15382303557"
    echo "  舒苗 - 15381150723"
    echo ""
    echo "登录方式：手机号 + 验证码"
    echo ""
    echo "查看日志：tail -f /tmp/trust-app.log"
    echo "停止服务：pkill -f 'python3 app.py'"
else
    echo "❌ 启动失败，查看日志："
    tail -20 /tmp/trust-app.log
fi
