# ZY-HR 变更日志

## [0.1.0] - 2026-07-19

### 新增
- backend/config.py：环境变量配置管理，从 .env 读取
- backend/models/db.py：统一数据库连接管理（支持 mock 模式）
- backend/utils/helpers.py：统一 JSON 响应格式（success/error）
- backend/routes/dashboard.py：dashboard 蓝图，迁移 /red_alert 和 /retirement_personnel_prediction 路由
- .env：环境变量文件（密码从代码迁移到环境变量）

### 优化
- backend/app.py：重构为 factory 模式 create_app()，支持 mock DB 标识
- 数据库密码从 zjyc_api.py 硬编码迁移到 .env

### 变更
- Flask 启动方式改为 config.py 集中管理配置
- API 路径保持原始 `/red_alert`（无 `/api` 前缀），前端无需修改
