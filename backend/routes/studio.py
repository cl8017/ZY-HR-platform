"""大师工作室 API — 工作室管理"""

from flask import Blueprint, request
from backend.models.db import db
from backend.utils.helpers import success, error

studio_bp = Blueprint('studio', __name__, url_prefix='/api')


@studio_bp.route('/zjyc/create_master_studio', methods=['POST'])
def create_master_studio():
    """创建大师工作室"""
    data = request.get_json()
    if not data:
        return error('请求体不能为空', 400)

    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO master_studio
                (studio_name, studio_master, description, category, created_at)
                VALUES (%s, %s, %s, %s, NOW())
            """, (
                data.get('studio_name', ''),
                data.get('studio_master', ''),
                data.get('description', ''),
                data.get('category', '')
            ))
            studio_id = cursor.lastrowid
    return success({'studio_id': studio_id}, '创建成功')
