# 部署运维

## 开发环境

### 前置条件

- Python 3.10+
- MySQL 8.0+
- Git

### 首次部署

```bash
# 1. 克隆代码
git clone https://github.com/cl8017/ZY-HR-platform.git
cd ZY-HR-platform

# 2. 安装依赖
pip3 install -r requirements.txt --break-system-packages

# 3. 配置数据库
vim .env  # 编辑数据库连接信息

# 4. 初始化数据库
python3 scripts/sync_schema.py init

# 5. 启动服务器
python3 backend/app.py
# 访问 http://localhost:58000
```

### 日常更新

```bash
# 一键部署（推荐）
python3 scripts/deploy.py --env test

# 或者手动
git pull origin main
pip3 install -r requirements.txt --break-system-packages
python3 scripts/sync_schema.py check  # 检查Schema
python3 scripts/sync_schema.py repair # 修复Schema
kill $(lsof -ti :58000) && python3 backend/app.py &
```

### 数据库管理

```bash
# 检查表结构完整性
python3 scripts/sync_schema.py check

# 修复表结构（添加缺失字段）
python3 scripts/sync_schema.py repair

# 重新初始化数据库（会清空数据）
python3 scripts/sync_schema.py init

# 数据迁移（从 yancao 库导入）
python3 scripts/migrate_data.py
```

---

## 生产环境部署

### 目录结构

```
/opt/ZY-HR/
├── backend/          # Flask 后端
├── static/           # 静态资源
├── pages/            # 前端页面
├── scripts/          # 运维脚本
├── docs/wiki/        # 文档
├── logs/             # 日志
├── .env              # 配置文件（不提交git）
├── requirements.txt
└── venv/             # Python 虚拟环境
```

### Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:58000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Systemd 服务

```ini
[Unit]
Description=ZY-HR Flask Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ZY-HR
EnvironmentFile=/opt/ZY-HR/.env
ExecStart=/opt/ZY-HR/venv/bin/gunicorn -w 4 -b 0.0.0.0:58000 backend.app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 数据库 Schema

### 业务表（zy_hr 库）

| 表名 | 说明 | 数据量 |
|------|------|--------|
| zy_hr_employee_roster | 员工花名册 | 509 |
| zy_hr_employee_profile | 员工档案 | 415 |
| zy_hr_red_alert | 红色预警 | 15 |
| zy_hr_retirement_prediction | 退休预测 | 153 |
| zy_hr_personnel_statistics | 编制统计 | 46 |
| zy_hr_competency_analysis | 胜任力分析 | 375 |
| zy_hr_talent_pool | 人才库 | 216 |
| zy_hr_teacher | 导师帮带 | 5 |
| zy_hr_score_record | 积分记录 | 4 |
| zy_hr_member | 积分成员 | 3 |
| zy_hr_master_studio | 大师工作室 | 2 |
| zy_hr_master_studio_member | 工作室成员 | 6 |
| zy_hr_group_project | 课题项目 | 2 |
| zy_hr_group_members | 项目成员 | 6 |
| zy_hr_group_phases | 项目阶段 | 5 |
| zy_hr_group_phase_content | 阶段内容 | 5 |
| zy_hr_group_achievements | 项目成果 | 4 |
| zy_hr_group_dashboards | 项目看板 | 2 |

### 系统表（yancao 库）

若依 RuoYi 系统表，提供用户认证和菜单管理：

| 表名 | 说明 |
|------|------|
| sys_user | 用户(5) |
| sys_role | 角色(3) |
| sys_menu | 菜单(222) |
| sys_dept | 部门(10) |
| sys_role_menu | 角色菜单关联(140) |

---

## 常用运维命令

```bash
# 查看日志
tail -f logs/app.log

# 重启服务
kill $(lsof -ti :58000) && python3 backend/app.py &

# 查看数据库状态
python3 scripts/sync_schema.py check
```
