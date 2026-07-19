"""路由模块注册"""

from backend.routes.dashboard import dashboard_bp
from backend.routes.talent import talent_bp
from backend.routes.teacher import teacher_bp
from backend.routes.studio import studio_bp
from backend.routes.project import project_bp

# 所有 Blueprint 列表（在 app.py 中注册）
all_blueprints = [
    dashboard_bp,
    talent_bp,
    teacher_bp,
    studio_bp,
    project_bp,
]
