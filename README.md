# 镇江烟草人才培养数智平台 (ZY-HR)

> Zhenjiang Tobacco HR Digital Platform

## 项目概述

镇江烟草「人才培养」数智平台，涵盖数据看板、人才库、导师帮带、大师工作室、课题项目组、文档查重、岗位胜任力七大模块。

## 技术栈

- **后端**: Flask + PyMySQL
- **前端**: 纯 HTML + Tailwind CSS + ECharts / Chart.js
- **数据库**: MySQL × 2 服务器
- **认证**: 若依 SSO

## 目录结构

```
ZY-HR/
├── backend/          # Flask 后端（模块化）
├── static/           # 静态资源
├── pages/            # 前端页面
├── scripts/          # 运维脚本
├── docs/wiki/        # 项目文档
├── .gitignore
├── requirements.txt
└── README.md
```

## 快速开始

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（从 .env.example 复制）
cp .env.example .env
# 编辑 .env 填入数据库配置

# 启动开发服务器
python3 backend/app.py
```

## 部署

参见 [docs/wiki/deployment.md](docs/wiki/deployment.md)
