"""导师帮带 API — 导师查询、员工事件、词云分析"""

from flask import Blueprint, request
from backend.models.db import db
from backend.utils.helpers import success, error

teacher_bp = Blueprint('teacher', __name__, url_prefix='')


@teacher_bp.route('/api/zjyc/teacher')
def get_related_people():
    """导师关系查询"""
    name = request.args.get('name', '')
    if not name:
        return error('缺少参数: name', 400)

    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            sql = """
                SELECT a.name, a.role, b.department, b.current_position
                FROM (
                    SELECT %s AS name, '员工' AS role FROM DUAL
                    UNION
                    SELECT teacher, type FROM tb_zjyc_teacher WHERE name = %s
                ) a
                LEFT JOIN employee_roster b ON a.name = b.name
            """
            cursor.execute(sql, (name, name))
            data = cursor.fetchall()
    return success(data)


@teacher_bp.route('/employee/events')
def employee_events():
    """员工事件查询"""
    name = request.args.get('name', '')
    if not name:
        return error('缺少参数: name', 400)

    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM employee_events WHERE name = %s ORDER BY event_date DESC",
                (name,)
            )
            data = cursor.fetchall()
    return success(data)


@teacher_bp.route('/person/wordcloud')
def person_wordcloud():
    """个人词云"""
    name = request.args.get('name', '')
    if not name:
        return error('缺少参数: name', 400)

    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT word, weight FROM person_wordcloud WHERE name = %s",
                (name,)
            )
            data = cursor.fetchall()
    return success(data)
