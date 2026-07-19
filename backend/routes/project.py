"""课题项目组 API — 项目CRUD、成员、阶段、成果管理"""

from flask import Blueprint, request
from datetime import datetime
from backend.models.db import db
from backend.utils.helpers import success, error, bad_request

project_bp = Blueprint('project', __name__, url_prefix='/api/group')


@project_bp.route('/projects')
def get_group_projects():
    """项目列表"""
    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            sql = """
                SELECT
                    p.project_id,
                    p.project_name,
                    p.project_description,
                    p.status,
                    p.start_date,
                    p.end_date,
                    p.created_at,
                    p.updated_at,
                    COALESCE(m.member_name, '-') as leader_name
                FROM tb_zjyc_group_project p
                LEFT JOIN tb_zjyc_group_members m
                    ON p.project_id = m.project_id AND m.member_type = 0
                ORDER BY p.created_at DESC
            """
            cursor.execute(sql)
            data = cursor.fetchall()
    return success(data)


@project_bp.route('/<int:project_id>')
def get_project_detail(project_id):
    """项目详情"""
    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM tb_zjyc_group_project WHERE project_id = %s",
                (project_id,)
            )
            data = cursor.fetchone()
    if not data:
        return error('项目不存在', 404)
    return success(data)


@project_bp.route('/<int:project_id>/members')
def get_project_members(project_id):
    """项目成员"""
    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM tb_zjyc_group_members WHERE project_id = %s ORDER BY sort_order",
                (project_id,)
            )
            data = cursor.fetchall()
    return success(data)


@project_bp.route('/<int:project_id>/phases')
def get_project_phases(project_id):
    """项目阶段（含阶段内容）"""
    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.*, c.content_id, c.content_title, c.content_type, c.content_text
                FROM tb_zjyc_group_phases p
                LEFT JOIN tb_zjyc_group_phase_content c
                    ON p.phase_id = c.phase_id
                WHERE p.project_id = %s
                ORDER BY p.sort_order, c.sort_order
            """, (project_id,))
            rows = cursor.fetchall()

    # 按阶段分组
    phases = {}
    for row in rows:
        pid = row['phase_id']
        if pid not in phases:
            phases[pid] = {
                'phase_id': pid,
                'phase_name': row['phase_name'],
                'phase_icon': row['phase_icon'],
                'start_date': row['start_date'],
                'end_date': row['end_date'],
                'phase_description': row['phase_description'],
                'contents': []
            }
        if row.get('content_id'):
            phases[pid]['contents'].append({
                'content_id': row['content_id'],
                'content_title': row['content_title'],
                'content_type': row['content_type'],
                'content_text': row['content_text']
            })
    return success(list(phases.values()))


@project_bp.route('/<int:project_id>/achievements')
def get_project_achievements(project_id):
    """项目成果"""
    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM tb_zjyc_group_achievements WHERE project_id = %s ORDER BY sort_order",
                (project_id,)
            )
            data = cursor.fetchall()
    return success(data)


@project_bp.route('/<int:project_id>/dashboard')
def get_project_dashboard(project_id):
    """项目看板统计"""
    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            # 成员数
            cursor.execute(
                "SELECT COUNT(*) AS count FROM tb_zjyc_group_members WHERE project_id = %s",
                (project_id,)
            )
            member_count = cursor.fetchone()['count']

            # 阶段数
            cursor.execute(
                "SELECT COUNT(*) AS count FROM tb_zjyc_group_phases WHERE project_id = %s",
                (project_id,)
            )
            phase_count = cursor.fetchone()['count']

            # 成果数
            cursor.execute(
                "SELECT COUNT(*) AS count FROM tb_zjyc_group_achievements WHERE project_id = %s",
                (project_id,)
            )
            achievement_count = cursor.fetchone()['count']

    return success({
        'memberCount': member_count,
        'phaseCount': phase_count,
        'achievementCount': achievement_count
    })


@project_bp.route('/create-project', methods=['POST'])
def create_project():
    """创建项目"""
    data = request.get_json()
    if not data:
        return bad_request('请求体不能为空')

    required = ['project_name', 'project_title', 'project_description']
    for field in required:
        if field not in data or not data[field]:
            return bad_request(f'缺少必填字段: {field}')

    now = datetime.now()
    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO tb_zjyc_group_project
                (project_name, project_title, project_description, project_intro1,
                 project_intro2, project_slogan, background_image,
                 start_date, end_date, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data['project_name'],
                data['project_title'],
                data['project_description'],
                data.get('project_intro1', ''),
                data.get('project_intro2', ''),
                data.get('project_slogan', ''),
                data.get('background_image', ''),
                data.get('start_date'),
                data.get('end_date'),
                data.get('status', 1),
                now, now
            ))
            project_id = cursor.lastrowid

            # 如果有负责人信息
            leader_name = data.get('leader_name')
            if leader_name:
                cursor.execute("""
                    INSERT INTO tb_zjyc_group_members
                    (project_id, member_name, member_title, member_image, member_type, sort_order)
                    VALUES (%s, %s, '项目负责人', '', 0, 0)
                """, (project_id, leader_name))

    return success({'project_id': project_id}, '创建成功')


@project_bp.route('/<int:project_id>/add-member', methods=['POST'])
def add_project_member(project_id):
    """添加项目成员"""
    data = request.get_json()
    if not data or 'member_name' not in data:
        return bad_request('缺少必填字段: member_name')

    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tb_zjyc_group_members
                (project_id, member_name, member_title, member_image, member_type, description, sort_order)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                project_id,
                data['member_name'],
                data.get('member_title', '团队成员'),
                data.get('member_image', ''),
                data.get('member_type', 1),
                data.get('description', ''),
                data.get('sort_order', 0)
            ))
            member_id = cursor.lastrowid
    return success({'member_id': member_id}, '添加成功')


@project_bp.route('/<int:project_id>/add-achievement', methods=['POST'])
def add_project_achievement(project_id):
    """添加项目成果"""
    data = request.get_json()
    if not data or 'achievement_name' not in data:
        return bad_request('缺少必填字段: achievement_name')

    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tb_zjyc_group_achievements
                (project_id, achievement_name, achievement_type, achievement_desc, achievement_date, sort_order)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                project_id,
                data['achievement_name'],
                data.get('achievement_type', '成果'),
                data.get('achievement_desc', ''),
                data.get('achievement_date'),
                data.get('sort_order', 0)
            ))
            achievement_id = cursor.lastrowid
    return success({'achievement_id': achievement_id}, '添加成功')


@project_bp.route('/statistics')
def get_group_statistics():
    """项目全局统计"""
    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM tb_zjyc_group_project")
            project_count = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as total FROM tb_zjyc_group_members")
            member_count = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as total FROM tb_zjyc_group_achievements")
            achievement_count = cursor.fetchone()['total']

            cursor.execute("""
                SELECT achievement_type, COUNT(*) as count
                FROM tb_zjyc_group_achievements
                GROUP BY achievement_type
            """)
            achievement_types = cursor.fetchall()

            cursor.execute("""
                SELECT member_type, COUNT(*) as count
                FROM tb_zjyc_group_members
                GROUP BY member_type
            """)
            member_types = cursor.fetchall()

    return success({
        'projectCount': project_count,
        'memberCount': member_count,
        'achievementCount': achievement_count,
        'achievementByType': {item['achievement_type']: item['count'] for item in achievement_types},
        'memberByType': {item['member_type']: item['count'] for item in member_types}
    })


@project_bp.route('/<int:project_id>/toggle-visibility', methods=['PUT'])
def toggle_project_visibility(project_id):
    """切换项目显示/隐藏"""
    data = request.get_json()
    if data is None or 'is_visible' not in data:
        return bad_request('缺少必要参数: is_visible')

    is_visible = data['is_visible']
    status = 1 if is_visible else 0

    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT project_id FROM tb_zjyc_group_project WHERE project_id = %s",
                (project_id,)
            )
            if not cursor.fetchone():
                return error('项目不存在', 404)

            cursor.execute(
                "UPDATE tb_zjyc_group_project SET status = %s WHERE project_id = %s",
                (status, project_id)
            )

    return success({'project_id': project_id, 'status': status}, '更新成功')
