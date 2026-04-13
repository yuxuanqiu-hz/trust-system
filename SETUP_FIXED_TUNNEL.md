# 🌐 配置固定公网地址指南

## 方案选择

### 方案 1：Cloudflare Tunnel（推荐，免费）
- ✅ 固定域名
- ✅ HTTPS 自动
- ✅ 免费
- ️ 需要 Cloudflare 账号

### 方案 2：购买域名 + 云服务器
- ✅ 完全控制
- ✅ 专业形象
- ❌ 需要付费

### 方案 3：内网穿透服务
- ✅ 简单快速
- ❌ 大多数需要付费

---

## 🚀 Cloudflare Tunnel 配置步骤

### 第 1 步：注册 Cloudflare 账号

1. 访问 https://www.cloudflare.com
2. 点击 "Sign Up" 注册免费账号
3. 验证邮箱

### 第 2 步：创建 Tunnel

**方法 A：通过网页创建（推荐）**

1. 登录 Cloudflare 控制台
2. 进入 **Zero Trust** → **Networks** → **Tunnels**
3. 点击 **Create a tunnel**
4. 选择 **Cloudflared**
5. 输入隧道名称：`trust-system`
6. 点击 **Save tunnel**
7. 选择您的操作系统：Linux → amd64
8. 复制安装命令

**方法 B：通过命令行创建**

```bash
# 1. 登录 Cloudflare
cd /tmp
./cloudflared-linux-amd64 tunnel login

# 2. 创建隧道
./cloudflared-linux-amd64 tunnel create trust-system

# 3. 获取隧道 ID
./cloudflared-linux-amd64 tunnel list
```

### 第 3 步：配置隧道

在 Cloudflare 控制台：

1. **Add a public hostname**
   - Subdomain: `trust` (或您想要的子域名)
   - Domain: `yourdomain.com` (或使用 cloudflare 提供的域名)
   - Service: `http://localhost:5001`
   - Type: `HTTP`

2. **保存配置**

### 第 4 步：安装连接器

在服务器执行 Cloudflare 提供的安装命令，例如：

```bash
# 示例命令（以 Cloudflare 控制台显示的为准）
./cloudflared-linux-amd64 service install eyJhIjoi...（您的 token）
```

### 第 5 步：启动服务

```bash
# 启动 tunnel 服务
sudo systemctl start cloudflared

# 设置开机自启
sudo systemctl enable cloudflared

# 查看状态
sudo systemctl status cloudflared
```

---

## 📋 配置文件

### /etc/cloudflared/config.yml

```yaml
tunnel: trust-system
credentials-file: /etc/cloudflared/credentials.json

ingress:
  - hostname: trust.yourcompany.com
    service: http://localhost:5001
  - service: http_status:404
```

### systemd 服务配置

```ini
[Unit]
Description=Cloudflare Tunnel
After=network.target

[Service]
Type=simple
User=admin
ExecStart=/tmp/cloudflared-linux-amd64 tunnel run trust-system
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 🎯 快速配置脚本

创建 `setup-fixed-tunnel.sh`：

```bash
#!/bin/bash
# Cloudflare Tunnel 固定地址配置脚本

echo "=== Cloudflare Tunnel 配置 ==="

# 1. 检查是否已登录
if [ ! -f ~/.cloudflared/cert.pem ]; then
    echo "请先登录 Cloudflare："
    echo "cd /tmp && ./cloudflared-linux-amd64 tunnel login"
    exit 1
fi

# 2. 创建隧道
TUNNEL_NAME="trust-system"
./cloudflared-linux-amd64 tunnel create $TUNNEL_NAME

# 3. 获取隧道 ID
TUNNEL_ID=$(./cloudflared-linux-amd64 tunnel list | grep $TUNNEL_NAME | awk '{print $2}')
echo "隧道 ID: $TUNNEL_ID"

# 4. 配置路由
./cloudflared-linux-amd64 tunnel route dns $TUNNEL_ID trust.yourcompany.com

# 5. 安装服务
./cloudflared-linux-amd64 service install

# 6. 启动服务
sudo systemctl start cloudflared
sudo systemctl enable cloudflared

echo "✅ 配置完成！"
echo "访问地址：https://trust.yourcompany.com"
```

---

## 🆘 常见问题

### Q1: 没有域名怎么办？

**解决：**
1. 在 Cloudflare 注册免费域名（部分 TLD 免费）
2. 或使用 Cloudflare 提供的快速隧道域名
3. 或购买便宜域名（.xyz 约$1/年）

### Q2: 隧道连接失败

**解决：**
```bash
# 检查隧道状态
sudo systemctl status cloudflared

# 查看日志
sudo journalctl -u cloudflared -f

# 重启服务
sudo systemctl restart cloudflared
```

### Q3: 如何更换域名

**解决：**
1. Cloudflare 控制台 → Tunnels
2. 编辑隧道配置
3. 修改 Public Hostname
4. 保存并等待生效

---

## 💰 费用说明

**Cloudflare Tunnel 免费额度：**
- ✅ 50 个隧道（免费）
- ✅ 无限流量
- ✅ HTTPS 自动
- ✅ 全球 CDN

**付费选项（可选）：**
- Cloudflare Pro: $20/月（高级功能）
- 域名注册：约$10-15/年

---

## 📞 下一步操作

1. **注册 Cloudflare 账号**
   - 访问：https://www.cloudflare.com

2. **创建 Tunnel**
   - 进入 Zero Trust 控制台
   - 创建名为 `trust-system` 的隧道

3. **配置域名**
   - 使用免费域名或自有域名
   - 配置 DNS 路由

4. **安装服务**
   - 复制安装命令到服务器执行
   - 启动 systemd 服务

5. **测试访问**
   - 访问配置的域名
   - 使用管理员账号登录

---

**需要我帮您执行哪一步？**
