#!/bin/bash
# ZY-HR 开发环境快速启动脚本
set -e

cd "$(dirname "$0")/.."

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate

# 安装依赖
if [ ! -f "venv/.deps_installed" ]; then
    echo "📥 安装依赖..."
    pip install -r requirements.txt -q
    touch venv/.deps_installed
fi

# 检查 .env
if [ ! -f ".env" ]; then
    echo "⚠️  未找到 .env 文件，正在从模板复制..."
    cp .env.example .env
    echo "✏️  请编辑 .env 填入数据库信息，然后重新启动"
    exit 1
fi

echo "🚀 启动 Flask 开发服务器 (端口 58000)..."
export FLASK_APP=backend/app.py
export FLASK_DEBUG=1
flask run --host 0.0.0.0 --port 58000
