#!/bin/bash
# 重启 Cloudflare Tunnel

echo "正在重启 Cloudflare Tunnel..."

# 停止旧进程
pkill -f cloudflared
sleep 2

# 启动新进程
cd /tmp
nohup ./cloudflared-linux-amd64 tunnel --url http://127.0.0.1:5001 > /tmp/cloudflared.log 2>&1 &

# 等待启动
sleep 8

# 获取公网地址
PUBLIC_URL=$(cat /tmp/cloudflared.log | grep -o 'https://[a-zA-Z0-9.-]*\.trycloudflare\.com' | head -1)

if [ -n "$PUBLIC_URL" ]; then
    echo "✅ Tunnel 重启成功！"
    echo ""
    echo "公网访问地址：$PUBLIC_URL"
    echo ""
    echo "管理员账号："
    echo "  裘宇轩 - 15382303557"
    echo "  舒苗 - 15381150723"
else
    echo "❌ Tunnel 启动失败，查看日志："
    tail -20 /tmp/cloudflared.log
fi
