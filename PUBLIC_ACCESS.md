# 🌐 信托管理系统 - 公网访问

## ✅ 公网访问已配置完成！

---

## 🔗 访问地址

### 公网 HTTPS 访问（推荐）
```
https://built-taste-nick-sponsorship.trycloudflare.com
```

### 公司内网访问
```
http://10.1.16.227:5001
```

### 本机访问
```
http://localhost:5001
```

---

## 👥 登录账号

### 管理员账号
| 姓名 | 手机号 | 角色 |
|------|--------|------|
| 裘宇轩 | 15382303557 | 管理员 |
| 舒苗 | 15381150723 | 管理员&员工 |

### 员工账号
35 名员工可使用手机号 + 验证码登录

---

## 🚀 如何使用

### 1. 首次访问
1. 打开浏览器访问：https://built-taste-nick-sponsorship.trycloudflare.com
2. 输入管理员手机号：15382303557
3. 点击"获取验证码"
4. 查看系统日志获取验证码：`tail -f /tmp/trust-app.log`
5. 输入验证码登录

### 2. 分享给其他人
将公网地址发送给需要访问的人员：
```
https://built-taste-nick-sponsorship.trycloudflare.com

管理员账号：
- 裘宇轩 15382303557
- 舒苗 15381150723
```

---

## 🔧 管理命令

### 查看 Tunnel 状态
```bash
ps aux | grep cloudflared
```

### 重启 Tunnel
```bash
pkill -f cloudflared
cd /tmp
nohup ./cloudflared-linux-amd64 tunnel --url http://127.0.0.1:5001 > /tmp/cloudflared.log 2>&1 &
sleep 8
cat /tmp/cloudflared.log | grep 'trycloudflare.com'
```

### 查看日志
```bash
# 应用日志
tail -f /tmp/trust-app.log

# Tunnel 日志
tail -f /tmp/cloudflared.log
```

### 停止服务
```bash
# 停止 Tunnel
pkill -f cloudflared

# 停止应用
pkill -f "python3 app.py"
```

---

## ⚠️ 重要提示

### 1. 有效期
- 当前使用的是 **临时隧道**
- 每次重启会生成不同的地址
- 如需固定地址，需注册 Cloudflare 账号

### 2. 安全配置
当前为测试环境，建议：
- ✅ 已启用 HTTPS 加密传输
- ⚠️ 验证码仍在日志中显示
- ⚠️ 无访问 IP 限制

### 3. 生产环境建议
如需长期使用，建议：
1. 注册 Cloudflare 账号配置固定隧道
2. 接入短信服务发送验证码
3. 配置访问 IP 白名单
4. 设置强密码策略

---

## 📱 员工登录流程

1. 访问：https://built-taste-nick-sponsorship.trycloudflare.com
2. 输入个人手机号
3. 点击"获取验证码"
4. 查看系统日志获取验证码
5. 输入验证码登录
6. 查看个人信托数据

---

## 🆘 常见问题

### Q1: 公网地址无法访问
**解决：**
```bash
# 检查应用是否运行
ps aux | grep "python3 app.py"

# 检查 Tunnel 是否运行
ps aux | grep cloudflared

# 重启 Tunnel
bash /home/admin/openclaw/workspace/trust-system/restart-tunnel.sh
```

### Q2: 验证码收不到
**当前配置：** 验证码显示在系统日志中
**查看方式：**
```bash
tail -f /tmp/trust-app.log
```

### Q3: 如何固定公网地址
需要注册 Cloudflare 账号：
1. 访问 https://www.cloudflare.com 注册
2. 创建 Tunnel 获取固定地址
3. 更新启动脚本

---

## 📞 技术支持

**系统目录：** `/home/admin/openclaw/workspace/trust-system/`

**配置文件：**
- 应用日志：`/tmp/trust-app.log`
- Tunnel 日志：`/tmp/cloudflared.log`
- 启动脚本：`/home/admin/openclaw/workspace/trust-system/`

**文档：**
- 部署指南：`DEPLOYMENT_GUIDE.md`
- 公网访问：`PUBLIC_ACCESS.md`

---

**配置时间：** 2026-04-13 19:15
**公网地址：** https://built-taste-nick-sponsorship.trycloudflare.com
**状态：** ✅ 运行中
