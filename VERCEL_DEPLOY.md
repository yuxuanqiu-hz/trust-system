# 信托管理系统 - Vercel 部署指南

## 🚀 部署方式

### 方式 1：通过 GitHub 部署（推荐）

#### 第 1 步：创建 GitHub 仓库

1. 访问 https://github.com
2. 点击右上角 **+** → **New repository**
3. 仓库名：`trust-system`
4. 设为 **Public** 或 **Private**
5. 点击 **Create repository**

#### 第 2 步：上传代码

```bash
cd /home/admin/openclaw/workspace/trust-system
git init
git add .
git commit -m "Initial commit - trust system"
git branch -M main
git remote add origin https://github.com/您的用户名/trust-system.git
git push -u origin main
```

#### 第 3 步：在 Vercel 部署

1. 访问 https://vercel.com
2. 点击 **Add New** → **Project**
3. 选择 **Import Git Repository**
4. 找到 `trust-system` 仓库
5. 点击 **Import**
6. 保持默认配置
7. 点击 **Deploy**

#### 第 4 步：等待部署完成

- 等待 2-5 分钟
- 部署成功后会显示访问地址
- 格式：`https://trust-system-xxx.vercel.app`

---

### 方式 2：Vercel CLI 部署

```bash
# 安装 Vercel CLI
npm install -g vercel

# 登录 Vercel
vercel login

# 进入项目目录
cd /home/admin/openclaw/workspace/trust-system

# 部署
vercel --prod
```

---

## 📁 部署文件说明

已创建的文件：
- `vercel.json` - Vercel 配置文件
- `vercel_app.py` - Vercel 入口文件
- `requirements.txt` - Python 依赖

---

## 🗄️ 数据库处理

**注意：** Vercel 是无服务器架构，SQLite 数据库无法持久化。

### 解决方案：

#### 方案 A：使用 Vercel Postgres（免费）

1. 在 Vercel 控制台添加 **Storage** → **Postgres**
2. 获取数据库连接字符串
3. 修改 `app.py` 中的数据库配置

#### 方案 B：使用 SQLite（临时）

- 每次部署后数据库会重置
- 适合测试，不适合生产

#### 方案 C：使用外部数据库

- 使用免费的 **Supabase** 或 **Railway** PostgreSQL
- 配置环境变量连接

---

## ⚠️ 重要提示

1. **数据库迁移**：需要将 SQLite 数据迁移到 PostgreSQL
2. **环境变量**：在 Vercel 设置中配置 `SECRET_KEY`
3. **域名**：免费域名格式为 `xxx.vercel.app`

---

## 🎯 推荐流程

1. **先用 GitHub 方式部署**（5 分钟）
2. **测试基本功能**
3. **配置 Vercel Postgres**（免费）
4. **迁移数据**

---

## 📞 需要帮助？

告诉我您选择哪种方式，我可以：
- 帮您准备 Git 命令
- 配置数据库连接
- 修改代码适配 Vercel
