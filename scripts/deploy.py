#!/usr/bin/env python3
"""
ZY-HR 一键部署脚本
用法: python3 scripts/deploy.py [--env production|test]
"""
import os
import sys
import subprocess
import argparse

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(cmd, cwd=None, check=True):
    """运行命令并打印输出"""
    print(f"  → {cmd}")
    r = subprocess.run(cmd, shell=True, cwd=cwd or PROJECT_DIR,
                       capture_output=True, text=True)
    if r.returncode != 0 and check:
        print(f"  ❌ 失败: {r.stderr.strip()}")
        sys.exit(1)
    if r.stdout.strip():
        print(f"     {r.stdout.strip()[:200]}")
    return r


def step(num, title):
    print(f"\n{'='*50}")
    print(f" Step {num}: {title}")
    print(f"{'='*50}")


def deploy(env='production'):
    print(f"\n🚀 ZY-HR 部署开始 (环境: {env})")
    print(f"   项目目录: {PROJECT_DIR}")

    # Step 1: Git 更新
    step(1, "拉取最新代码")
    run("git pull origin main")

    # Step 2: 安装依赖
    step(2, "安装 Python 依赖")
    pip = os.path.join(PROJECT_DIR, 'venv', 'bin', 'pip') if os.path.exists(
        os.path.join(PROJECT_DIR, 'venv')) else 'pip3'
    run(f"{pip} install -r requirements.txt --break-system-packages")

    # Step 3: 数据库检查/修复
    step(3, "数据库 Schema 检查")
    r = subprocess.run(
        [sys.executable, 'scripts/sync_schema.py', 'check'],
        cwd=PROJECT_DIR, capture_output=True, text=True
    )
    print(r.stdout)
    if r.returncode != 0:
        print("  ⚠️ Schema 异常，执行修复...")
        subprocess.run(
            [sys.executable, 'scripts/sync_schema.py', 'repair'],
            cwd=PROJECT_DIR
        )

    # Step 4: 停止旧服务
    step(4, "停止旧服务")
    run("kill $(lsof -ti :58000) 2>/dev/null || true", check=False)

    # Step 5: 启动新服务
    step(5, "启动 Flask 服务器")
    if env == 'production':
        # 生产模式用 gunicorn
        run("nohup gunicorn -w 4 -b 0.0.0.0:58000 "
            "--access-logfile logs/access.log "
            "--error-logfile logs/error.log "
            "backend.app:app > /dev/null 2>&1 &")
        print("  🌐 生产模式: gunicorn (4 workers)")
    else:
        # 测试模式用 Flask dev server
        run("nohup python3 backend/app.py > logs/app.log 2>&1 &")
        print("  🧪 测试模式: Flask dev server")

    # Step 6: 健康检查
    step(6, "健康检查")
    import time
    time.sleep(2)
    r = subprocess.run(
        "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:58000/api/health",
        shell=True, capture_output=True, text=True, timeout=10
    )
    if r.stdout.strip() == '200':
        print("  ✅ 服务启动成功! http://127.0.0.1:58000")
    else:
        print(f"  ❌ 健康检查失败: HTTP {r.stdout.strip()}")
        sys.exit(1)

    print(f"\n🎉 部署完成! 访问 http://127.0.0.1:58000")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ZY-HR 部署脚本')
    parser.add_argument('--env', default='production',
                       choices=['production', 'test'])
    args = parser.parse_args()
    deploy(args.env)
