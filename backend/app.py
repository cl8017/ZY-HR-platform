"""
ZY-HR Flask 应用入口
"""
import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

from backend.config import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app():
    app = Flask(__name__,
                static_folder=os.path.join(BASE_DIR, 'static'),
                template_folder=os.path.join(BASE_DIR, 'pages'))

    CORS(app)
    app.config['BASE_DIR'] = BASE_DIR
    app.config['SECRET_KEY'] = config.secret_key

    # 健康检查
    @app.route('/api/health')
    def health():
        return jsonify({
            "status": "ok",
            "project": "ZY-HR",
            "mock_db": config.mock_db,
            "version": "0.1.0"
        })

    # 前端页面目录（按优先级：pages/ 新目录 > 根目录旧文件）
    PAGES_DIRS = [
        os.path.join(BASE_DIR, 'pages'),
        BASE_DIR
    ]

    @app.route('/')
    def index():
        for d in PAGES_DIRS:
            path = os.path.join(d, 'index.html')
            if os.path.exists(path):
                return send_from_directory(d, 'index.html')
        return jsonify({"error": "index.html not found"}), 404

    @app.route('/<path:filename>')
    def serve_pages(filename):
        for d in PAGES_DIRS:
            path = os.path.join(d, filename)
            if os.path.exists(path):
                return send_from_directory(d, filename)
        return send_from_directory(BASE_DIR, filename), 404

    # 注册蓝图
    from backend.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from backend.routes.report import report_bp
    app.register_blueprint(report_bp)

    from backend.routes.teacher import teacher_bp
    app.register_blueprint(teacher_bp)

    from backend.routes.talent import talent_bp
    app.register_blueprint(talent_bp)

    from backend.routes.project import project_bp
    app.register_blueprint(project_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    print(f"🚀 ZY-HR v0.1.0 开发服务器启动: http://{config.host}:{config.port}")
    print(f"📦 Mock DB: {'ON' if config.mock_db else 'OFF'} (设置 MOCK_DB=0 连接真实数据库)")
    app.run(host=config.host, port=config.port, debug=config.debug)
