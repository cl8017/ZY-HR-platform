"""应用主入口 — Flask Application Factory"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.config import config
from backend.routes import all_blueprints


def create_app() -> Flask:
    """创建 Flask 应用实例"""
    app = Flask(__name__,
                static_folder='../static',
                static_url_path='/static')

    # === 基本配置 ===
    app.secret_key = config.secret_key
    app.debug = config.debug

    # === CORS ===
    CORS(app)

    # === 日志 ===
    _setup_logging(app)

    # === 注册 Blueprint ===
    for bp in all_blueprints:
        app.register_blueprint(bp)

    # === 静态文件路由（用于开发环境） ===
    @app.route('/')
    def serve_index():
        return send_from_directory('../pages', 'index.html')

    @app.route('/<path:filename>')
    def serve_pages(filename):
        # 先尝试 pages 目录
        pages_dir = Path(__file__).parent.parent / 'pages'
        file_path = pages_dir / filename
        if file_path.exists():
            return send_from_directory(str(pages_dir), filename)
        # 再尝试 static 目录
        static_dir = Path(__file__).parent.parent / 'static'
        return send_from_directory(str(static_dir), filename)

    # === 错误处理 ===
    @app.errorhandler(404)
    def not_found(e):
        return {'code': 404, 'msg': '接口不存在', 'data': None}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {'code': 500, 'msg': '服务器内部错误', 'data': None}, 500

    return app


def _setup_logging(app):
    """配置日志"""
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)

    handler = RotatingFileHandler(
        str(log_dir / 'zj-hr.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(module)s: %(message)s'
    ))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('应用启动完成')


# 应用实例（供 gunicorn 加载）
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=58000, debug=config.debug)
