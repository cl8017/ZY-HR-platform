# 部署运维

> 部署环境配置、启动方式、运维管理说明。

---

## 一、部署方式

### 1.1 当前部署（原始方式）

```bash
# 启动 Flask API（后端）
cd /mnt/c/code/ZY-HR
python zjyc_api.py

# 另启一个终端，启动静态文件服务
python http.server.py 8000
```

**问题**:
- 需要两个终端 / 两个进程
- 无后台守护，终端关闭服务即停止
- 无自动重启

### 1.2 推荐部署重构后

#### 方案 A：Flask 托管一切（适合轻量部署）

```
Flask API Server (gunicorn)
├── /api/* → 后端业务路由
└── / → 静态文件 (不存在的路由 fallback 到静态)
```

#### 方案 B：Nginx + Gunicorn（生产推荐）

```
Nginx (:80/:443)
├── /api/* → proxy_pass Gunicorn :58000
├── /static/* → 直接 serve 文件
└── /* → index.html SPA 入口
```

---

## 二、环境配置

### 2.1 环境变量

创建 `.env` 文件在项目根目录：

```bash
# 数据库配置1（主业务库）
DB_HOST=210.16.170.156
DB_PORT=3306
DB_USER=zj-yancao
DB_PASSWORD=your_password
DB_NAME=zj-yancao

# 数据库配置2（备用库）
DB2_HOST=36.149.161.6
DB2_PORT=33973
DB2_USER=root
DB2_PASSWORD=your_password
DB2_NAME=yancao

# 应用配置
SECRET_KEY=random-secret-key-change-me
FLASK_DEBUG=0

# 外部系统
RUOYI_BASE_URL=http://36.149.161.6:18114
STATIC_BASE_URL=http://210.16.170.156:58000
```

### 2.2 Python 依赖

```txt
# requirements.txt
Flask==3.1.0
flask-cors==5.0.1
PyMySQL==1.1.1
python-dotenv==1.1.0
python-multipart==0.0.20
gunicorn==23.0.0
```

### 2.3 Virtualenv 设置

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 三、启动命令

### 3.1 开发模式

```bash
# 加载环境变量
export $(grep -v '^#' .env | xargs)

# 启动
python backend/app.py
# 或
flask --app backend/app --debug run --port 58000
```

### 3.2 生产模式

```bash
# Gunicorn 启动
source venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:58000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --log-level info \
  backend.app:app
```

---

## 四、Systemd 服务（生产环境）

### 4.1 创建服务文件

```ini
# /etc/systemd/system/zj-hr.service
[Unit]
Description=ZY-HR Talent Platform Backend
After=network.target mysql.service
Wants=mysql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ZY-HR
EnvironmentFile=/opt/ZY-HR/.env
ExecStart=/opt/ZY-HR/venv/bin/gunicorn \
  -w 4 \
  -b 0.0.0.0:58000 \
  --access-logfile /var/log/zj-hr/access.log \
  --error-logfile /var/log/zj-hr/error.log \
  --log-level info \
  --max-requests 10000 \
  --max-requests-jitter 1000 \
  --timeout 120 \
  backend.app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4.2 管理命令

```bash
# 启用服务
sudo systemctl daemon-reload
sudo systemctl enable zj-hr
sudo systemctl start zj-hr

# 查看状态
sudo systemctl status zj-hr

# 查看日志
sudo journalctl -u zj-hr -f
sudo tail -f /var/log/zj-hr/error.log

# 重启
sudo systemctl restart zj-hr
```

---

## 五、日志配置

```python
# backend/config.py 中的日志配置
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    handler = RotatingFileHandler(
        'logs/zj-hr.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(module)s: %(message)s'
    ))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
```

---

## 六、Nginx 反向代理（推荐）

```nginx
# /etc/nginx/sites-available/zj-hr
server {
    listen 80;
    server_name your-domain.com;
    client_max_body_size 50M;

    # API 请求转发到 Gunicorn
    location /api/ {
        proxy_pass http://127.0.0.1:58000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态资源
    location /static/ {
        alias /opt/ZY-HR/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 前端页面
    location / {
        alias /opt/ZY-HR/pages/;
        try_files $uri $uri/ /index.html;
    }
}
```

---

## 七、运维检查清单

### 7.1 日常运维

- [ ] 检查 gunicorn 进程是否运行: `ps aux | grep gunicorn`
- [ ] 检查数据库连接: `curl http://localhost:58000/api/health`
- [ ] 查看错误日志: `tail -30 logs/error.log`
- [ ] 磁盘空间: `df -h`

### 7.2 部署流程

```bash
# 1. 拉取最新代码
cd /opt/ZY-HR
git pull

# 2. 更新依赖
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 3. 重启服务
sudo systemctl restart zj-hr

# 4. 验证
sleep 3 && curl http://localhost:58000/api/health
```

### 7.3 回滚流程

```bash
cd /opt/ZY-HR
git revert HEAD
sudo systemctl restart zj-hr
```

---

## 八、相关文档

- [[architecture|系统架构]]
- [[refactoring-plan|重构方案#部署配置]]
