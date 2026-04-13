#!/bin/bash
# 信托管理系统 - 快速公网访问部署

echo "============================================================"
echo "信托管理系统 - 快速公网访问"
echo "============================================================"

# 获取本机 IP
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo "本机 IP: $LOCAL_IP"

# 1. 确保服务运行
echo ""
echo "[1/3] 启动信托管理系统..."
cd /home/admin/openclaw/workspace/trust-system
pkill -f "python3 app.py" 2>/dev/null || true
sleep 1
nohup python3 app.py > /tmp/trust-app.log 2>&1 &
sleep 3

# 检查服务
if curl -s http://localhost:5001/login > /dev/null 2>&1; then
    echo "  ✓ 服务已启动"
else
    echo "  ✗ 服务启动失败"
    exit 1
fi

# 2. 配置防火墙
echo ""
echo "[2/3] 配置防火墙..."
if command -v ufw &> /dev/null; then
    ufw allow 5001/tcp 2>/dev/null || true
    echo "  ✓ 已开放 5001 端口"
else
    echo "  ⚠️  未检测到 UFW，请手动开放 5001 端口"
fi

# 3. 显示访问信息
echo ""
echo "[3/3] 生成访问信息..."
echo ""
echo "============================================================"
echo "✅ 部署完成！"
echo "============================================================"
echo ""
echo "访问方式："
echo ""
echo "1️⃣  局域网访问（公司内网）："
echo "   http://$LOCAL_IP:5001"
echo ""
echo "2️⃣  本机访问："
echo "   http://localhost:5001"
echo ""
echo "3️⃣  公网访问（需要配置端口转发）："
echo "   - 在路由器配置端口转发：5001 -> $LOCAL_IP:5001"
echo "   - 或使用内网穿透工具（如 ngrok, frp）"
echo ""
echo "管理员账号："
echo "  裘宇轩 - 15382303557"
echo "  舒苗 - 15381150723"
echo ""
echo "管理命令："
echo "  查看日志：tail -f /tmp/trust-app.log"
echo "  停止服务：pkill -f 'python3 app.py'"
echo "  重启服务：bash $0"
echo ""
echo "⚠️  安全提示："
echo "  1. 当前为 HTTP 明文传输，建议配置 HTTPS"
echo "  2. 验证码在日志中显示，生产环境需接入短信服务"
echo "  3. 建议在防火墙限制访问 IP"
echo "============================================================"
