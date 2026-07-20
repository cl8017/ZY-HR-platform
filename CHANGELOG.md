# ZY-HR 变更日志

## [0.3.1] - 2026-07-20

### 修复
- 登录接口 `access_token` 从嵌套 `data` 移到顶层，前端 `setToken(data.access_token)` 能正确获取
- 菜单路由 `_build_menu_tree` 缺失 `name` 字段导致 `permission.ts` 崩溃（Cannot read undefined.toString）
- 菜单路由 path 缺少前导 `/` 导致 Vue Router 报错（"rencai" should be "/rencai"）
- 多路由派生同名导致前端报"路由名称重复"（通过去重计数器自动加 _2 / _3 后缀）
- 租户接口 `/auth/tenant/list` 返回 `data: []` 而非 `data: {tenantEnabled: false, voList: []}`
- 前端 `duplicateRouteChecker` 增加 `route.name?.toString()` 空安全保护

### 变更
- `backend/routes/system.py`: `_derive_route_name()` 新增从组件路径派生 name，`_normalize_path()` 增加前导 /
- `backend/routes/auth.py`: login 接口 access_token 顶层返回；tenant_list 格式对齐前端预期

## [0.3.0] - 2026-07-19

### 新增
- backend/routes/teacher.py：导师帮带蓝图（/employee/events, /person/wordcloud, /api/zjyc/teacher）
- backend/routes/talent.py：人才库+大师工作室蓝图（/api/zjyc/score, /api/zjyc/create_master_studio, /api/zjyc/count_by_category, /api/board/talent/category）
- backend/routes/project.py：课题项目组蓝图（/api/group/projects, /api/group/<id>, /api/group/<id>/members, /api/group/<id>/phases, /api/group/<id>/achievements, /api/group/<id>/dashboard, /api/group/create-project, /api/group/<id>/add-member, /api/group/<id>/add-achievement, /api/group/statistics, /api/group/<id>/toggle-visibility）
- MockCursor 扩展支持 teacher / talent / project 相关 mock 数据

### 优化
- backend/app.py 注册 teacher/talent/project 三个新蓝图
- API 路径保持原始，前端无需修改

## [0.2.0] - 2026-07-19

### 新增
- backend/routes/report.py：编制/预警/花名册蓝图（/compilation, /red_alert_department, /employee_roster_markdown）
- backend/utils/text_utils.py：文本工具函数（camel_case, preprocess_text, parse_event_field 抽取）
- /position_competency_analysis 路由迁移到 dashboard.py（使用 db2）
- 输入参数校验（int 转换异常返回 HTTP 400）
- MockCursor 扩展支持 compilation, employee_roster, department 预警, position_competency 的 mock 数据

### 修复
- MockCursor 缺少 __enter__/__exit__ 导致路由报 500
- position_competency_analysis 缺少 jsonify 导入
- int() 参数转换无校验导致 abc 等非法输入 500 崩

### 优化
- db2 改为惰性导入（函数内部 import），避免模块加载时连接
- 所有新增路由保留原始响应格式（json.dumps 或 jsonify 原始数组），前端兼容

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
- API 路径保持原始，前端无需修改
