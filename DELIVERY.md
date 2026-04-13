# 信托管理系统 - 交付文档

## ✅ 已完成工作

### 1. 数据文件分析

**文件：** `共享文件/信托最新情况 20260328-V2.xlsx`

**数据结构：**
- **工作表：** 汇总表（39 行，45 列）、明细表（空）
- **核心字段：**
  - 员工信息：姓名、工号
  - 授予信息：锁定期、授予数、已归属数、已归属比例
  - 分配信息：第一次分配、第二次分配、累计数
  - 行权卖股：剩余可行权股数、卖股收益、卖股缴税
  - 问卷信息：问卷类型、是否行权、是否卖股等

### 2. 系统功能

**信托管理系统** (`/home/admin/openclaw/workspace/trust-system/`)

#### 核心功能
1. **登录系统**
   - 手机号 + 密码登录
   - 角色区分：管理员 (admin) / 普通用户 (user)

2. **权限管理**
   - 管理员：可查看所有数据、导入数据、管理用户
   - 普通用户：仅可查看自己的信托数据

3. **数据管理**
   - Excel 批量导入
   - 数据查询/搜索
   - 按工号关联用户

4. **用户管理**
   - 添加/编辑用户
   - 设置角色权限
   - 关联工号

### 3. 数据库设计

**users 表** - 用户信息
- id, username, phone, password_hash
- employee_no, name, role, department
- is_active, created_at

**trust_data 表** - 信托数据
- 员工信息：employee_no, name
- 授予信息：lock_period, grant_shares, vested_shares, vested_ratio
- 分配信息：first_*, second_*, total_*
- 卖股信息：remaining_exercisable, sell_income, sell_tax
- 问卷信息：survey_type, is_exercised, is_sold 等

---

## 🚀 如何启动系统

### 方法一：一键启动

```bash
cd /home/admin/openclaw/workspace/trust-system
python3 app.py
```

访问：http://localhost:5001

### 默认管理员账号
- **手机号：** 13800138000
- **密码：** admin123

---

## 📋 下一步工作

### 1. 完善管理界面模板

需要创建以下模板文件：
- `templates/dashboard.html` - 管理员仪表盘
- `templates/employee_dashboard.html` - 员工个人仪表盘
- `templates/users.html` - 用户管理列表
- `templates/user_form.html` - 用户添加/编辑表单
- `templates/data.html` - 数据管理列表
- `templates/import.html` - 数据导入页面

### 2. 导入初始数据

从 Excel 文件导入 39 条信托数据到数据库

### 3. 添加用户账号

为员工创建登录账号，关联工号：
```python
# 示例：添加用户
user = User(
    username='gongxin',
    phone='13800000001',
    employee_no='278055',  # 龚昕的工号
    name='龚昕',
    role='user'
)
user.set_password('123456')
```

### 4. 功能增强（可选）

- [ ] 数据导出（Excel）
- [ ] 数据统计图表
- [ ] 批量更新数据
- [ ] 操作日志
- [ ] 数据版本管理

---

## 📊 数据字段映射

| Excel 列名 | 数据库字段 |
|-----------|-----------|
| 姓名 | name |
| 工号 | employee_no |
| 锁定期 | lock_period |
| 授予数 | grant_shares |
| 已归属数 | vested_shares |
| 已归属（新） | vested_shares_new |
| 已归属比例 | vested_ratio |
| 第一次分配 - 行权数 | first_exercise_shares |
| 第一次分配 - 出售数 | first_sold_shares |
| 第一次分配 - 交易收入 | first_income |
| ... | ... |
| 累计 - 行权数 | total_exercise_shares |
| 累计 - 分配金额 | total_allocated |
| 问卷类型 | survey_type |
| 是否行权 | is_exercised |
| 是否卖股 | is_sold |

---

## 🔐 安全说明

1. **密码加密：** 使用 Werkzeug 的 password_hash
2. **权限隔离：** 管理员和普通用户数据隔离
3. **会话管理：** Flask-Login 会话管理
4. **生产环境：** 需修改 SECRET_KEY，使用 HTTPS

---

**交付时间：** 2026-04-11  
**系统版本：** v0.1 (MVP)  
**状态：** 核心功能完成，待完善 UI
