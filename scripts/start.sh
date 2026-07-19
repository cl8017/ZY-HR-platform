#!/bin/bash
# ZY-HR 生产环境启动脚本
set -e

cd "$(dirname "$0")/.."
source venv/bin/activate

mkdir -p logs

echo "🚀 启动 Gunicorn (4 workers, :58000)..."
exec gunicorn -w 4 -b 0.0.0.0:58000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --log-level info \
  --max-requests 10000 \
  --max-requests-jitter 1000 \
  --timeout 120 \
  backend.app:app
