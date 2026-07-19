# 镇江烟草人才培养数智平台（重构版）

> ZY-HR (Zhenjiang Tobacco HR Digital Platform) — 重构版本

## 项目说明

本项目为镇江烟草"人才培养"数智平台的完整重构。在保持现有功能的前提下，将单文件 Flask 应用改造为模块化架构，统一前端设计体系，并解决安全风险。

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端框架 | Flask + Blueprints |
| 数据库 | MySQL + PyMySQL (连接池) |
| 配置管理 | python-dotenv |
| 前端 | HTML + TailwindCSS + ECharts |
| 部署 | Gunicorn + systemd |

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/cl8017/ZY-HR-platform.git
cd ZY-HR-platform

# 2. 配置环境
cp .env.example .env
# 编辑 .env 填入数据库信息

# 3. 安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. 启动开发服务器
flask --app backend/app --debug run --port 58000
```

## 项目结构

```
ZY-HR-platform/
├── backend/              # 后端（Flask Blueprints）
│   ├── app.py            # 应用入口
│   ├── config.py         # 配置管理
│   ├── models/db.py      # 数据库连接池
│   ├── routes/           # 路由模块
│   │   ├── dashboard.py  # 数据看板 API
│   │   ├── talent.py     # 人才库 API
│   │   ├── teacher.py    # 导师帮带 API
│   │   ├── studio.py     # 大师工作室 API
│   │   ├── project.py    # 课题项目组 API
│   │   └── ddc.py        # 文档查重 API
│   ├── services/         # 业务逻辑层
│   └── utils/helpers.py  # 工具函数
├── static/               # 前端静态资源
│   ├── css/main.css      # 主题变量 + 全局样式
│   ├── js/api.js         # API 请求封装
│   └── js/utils.js       # 工具函数
├── pages/                # 前端页面
├── docs/                 # 文档
│   └── wiki/             # 项目 Wiki
├── scripts/              # 运维脚本
├── .env.example          # 环境变量模板
├── requirements.txt      # Python 依赖
└── README.md             # 本文件
```

## 重构路线

1. **Phase 1** — 基础设施与清理（目录结构、配置管理、废弃文件清理）
2. **Phase 2** — 后端重构（Blueprint 拆分、路由迁移）
3. **Phase 3** — 前端重构（统一设计体系、公共组件）
4. **Phase 4** — 安全加固与运维

详见 [docs/wiki/](docs/wiki/)
