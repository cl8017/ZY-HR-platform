"""project 模块 - 课题项目组路由（11个路由）"""
from flask import Blueprint, request
from backend.models.db import db1
from backend.utils.helpers import success, error

project_bp = Blueprint('project', __name__)


@project_bp.route('/api/group/projects', methods=['GET'])
def get_projects():
    """1. 获取所有课题项目"""
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM tb_zjyc_group_project ORDER BY sort_order ASC")
                projects = cursor.fetchall()
        return success(projects, '查询成功')
    except Exception as e:
        return error(f'查询失败: {str(e)}', 500)


@project_bp.route('/api/group/<int:project_id>', methods=['GET'])
def get_project_detail(project_id):
    """2. 获取课题项目详情（含成员、阶段、阶段内容、成就、仪表盘）"""
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                # 项目基本信息
                cursor.execute("SELECT * FROM tb_zjyc_group_project WHERE project_id = %s", (project_id,))
                project = cursor.fetchone()
                if not project:
                    return error('项目不存在', 404)

                # 成员列表
                cursor.execute(
                    "SELECT * FROM tb_zjyc_group_members WHERE project_id = %s ORDER BY member_id ASC",
                    (project_id,)
                )
                members = cursor.fetchall()

                # 阶段列表
                cursor.execute(
                    "SELECT * FROM tb_zjyc_group_phases WHERE project_id = %s ORDER BY phase_order ASC",
                    (project_id,)
                )
                phases = cursor.fetchall()

                # 阶段内容
                cursor.execute(
                    "SELECT * FROM tb_zjyc_group_phase_content WHERE project_id = %s ORDER BY phase_content_id ASC",
                    (project_id,)
                )
                phaseContents = cursor.fetchall()

                # 成就列表
                cursor.execute(
                    "SELECT * FROM tb_zjyc_group_achievements WHERE project_id = %s ORDER BY achievement_id ASC",
                    (project_id,)
                )
                achievements = cursor.fetchall()

                # 仪表盘
                cursor.execute(
                    "SELECT * FROM tb_zjyc_group_dashboards WHERE project_id = %s",
                    (project_id,)
                )
                dashboard = cursor.fetchone()
                if not dashboard:
                    dashboard = {
                        'member_count': len(members),
                        'phase_count': len(phases),
                        'achievement_count': len(achievements),
                    }

        data = {
            'project': project,
            'members': members,
            'phases': phases,
            'phaseContents': phaseContents,
            'achievements': achievements,
            'dashboard': dashboard,
        }
        return success(data, '查询成功')
    except Exception as e:
        return error(f'查询失败: {str(e)}', 500)


@project_bp.route('/api/group/<int:project_id>/members', methods=['GET'])
def get_project_members(project_id):
    """3. 获取课题项目成员列表"""
    try:
        member_type = request.args.get('memberType')
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                if member_type:
                    cursor.execute(
                        "SELECT * FROM tb_zjyc_group_members WHERE project_id = %s AND member_type = %s ORDER BY member_id ASC",
                        (project_id, member_type)
                    )
                else:
                    cursor.execute(
                        "SELECT * FROM tb_zjyc_group_members WHERE project_id = %s ORDER BY member_id ASC",
                        (project_id,)
                    )
                members = cursor.fetchall()
        return success(members, '查询成功')
    except Exception as e:
        return error(f'查询失败: {str(e)}', 500)


@project_bp.route('/api/group/<int:project_id>/phases', methods=['GET'])
def get_project_phases(project_id):
    """4. 获取课题项目阶段列表（含每个阶段的阶段内容）"""
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM tb_zjyc_group_phases WHERE project_id = %s ORDER BY phase_order ASC",
                    (project_id,)
                )
                phases = cursor.fetchall()

                # 为每个阶段查询对应的阶段内容
                for phase in phases:
                    cursor.execute(
                        "SELECT * FROM tb_zjyc_group_phase_content WHERE phase_id = %s ORDER BY phase_content_id ASC",
                        (phase['phase_id'],)
                    )
                    phase['contents'] = cursor.fetchall()

        return success(phases, '查询成功')
    except Exception as e:
        return error(f'查询失败: {str(e)}', 500)


@project_bp.route('/api/group/<int:project_id>/achievements', methods=['GET'])
def get_project_achievements(project_id):
    """5. 获取课题项目成就列表（含统计）"""
    try:
        achievement_type = request.args.get('type')
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                if achievement_type:
                    cursor.execute(
                        "SELECT * FROM tb_zjyc_group_achievements WHERE project_id = %s AND type = %s ORDER BY achievement_id ASC",
                        (project_id, achievement_type)
                    )
                else:
                    cursor.execute(
                        "SELECT * FROM tb_zjyc_group_achievements WHERE project_id = %s ORDER BY achievement_id ASC",
                        (project_id,)
                    )
                achievements = cursor.fetchall()

                # 统计
                cursor.execute(
                    "SELECT COUNT(*) AS total FROM tb_zjyc_group_achievements WHERE project_id = %s",
                    (project_id,)
                )
                total = cursor.fetchone()['total']

                cursor.execute(
                    "SELECT type, COUNT(*) AS count FROM tb_zjyc_group_achievements WHERE project_id = %s GROUP BY type",
                    (project_id,)
                )
                by_type = cursor.fetchall()

        data = {
            'achievements': achievements,
            'statistics': {
                'total': total,
                'byType': by_type,
            },
        }
        return success(data, '查询成功')
    except Exception as e:
        return error(f'查询失败: {str(e)}', 500)


@project_bp.route('/api/group/<int:project_id>/dashboard', methods=['GET'])
def get_project_dashboard(project_id):
    """6. 获取课题项目仪表盘数据（无则自动统计）"""
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM tb_zjyc_group_dashboards WHERE project_id = %s",
                    (project_id,)
                )
                dashboard = cursor.fetchone()

                if not dashboard:
                    cursor.execute(
                        "SELECT COUNT(*) AS cnt FROM tb_zjyc_group_members WHERE project_id = %s",
                        (project_id,)
                    )
                    member_cnt = cursor.fetchone()['cnt']

                    cursor.execute(
                        "SELECT COUNT(*) AS cnt FROM tb_zjyc_group_phases WHERE project_id = %s",
                        (project_id,)
                    )
                    phase_cnt = cursor.fetchone()['cnt']

                    cursor.execute(
                        "SELECT COUNT(*) AS cnt FROM tb_zjyc_group_achievements WHERE project_id = %s",
                        (project_id,)
                    )
                    achievement_cnt = cursor.fetchone()['cnt']

                    dashboard = {
                        'project_id': project_id,
                        'member_count': member_cnt,
                        'phase_count': phase_cnt,
                        'achievement_count': achievement_cnt,
                    }

        return success(dashboard, '查询成功')
    except Exception as e:
        return error(f'查询失败: {str(e)}', 500)


@project_bp.route('/api/group/create-project', methods=['POST'])
def create_project():
    """7. 创建新的课题项目（可选添加组长和成员）"""
    try:
        data = request.get_json()
        if not data:
            return error('请求数据不能为空', 400)

        project_name = data.get('project_name')
        if not project_name:
            return error('项目名称不能为空', 400)

        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                # 构建动态插入字段
                fields = ['project_name']
                values = [project_name]
                placeholders = ['%s']

                for field in ['description', 'leader', 'status', 'sort_order', 'start_date', 'end_date']:
                    if field in data:
                        fields.append(field)
                        values.append(data[field])
                        placeholders.append('%s')

                sql = f"INSERT INTO tb_zjyc_group_project ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
                cursor.execute(sql, tuple(values))
                project_id = cursor.lastrowid

                # 可选：添加组长
                leader = data.get('leader')
                if leader:
                    cursor.execute(
                        "INSERT INTO tb_zjyc_group_members (project_id, user_name, member_type) VALUES (%s, %s, %s)",
                        (project_id, leader, 'leader')
                    )

                # 可选：添加成员列表
                members = data.get('members', [])
                if isinstance(members, list):
                    for member in members:
                        cursor.execute(
                            "INSERT INTO tb_zjyc_group_members (project_id, user_name, member_type) VALUES (%s, %s, %s)",
                            (project_id, member.get('user_name', ''), member.get('member_type', 'member'))
                        )

        return success({'project_id': project_id, 'project_name': project_name}, '项目创建成功')
    except Exception as e:
        return error(f'项目创建失败: {str(e)}', 500)


@project_bp.route('/api/group/<int:project_id>/add-member', methods=['POST'])
def add_project_member(project_id):
    """8. 添加课题项目成员"""
    try:
        data = request.get_json()
        if not data:
            return error('请求数据不能为空', 400)

        user_name = data.get('user_name')
        if not user_name:
            return error('用户名称不能为空', 400)

        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                # 检查项目是否存在
                cursor.execute("SELECT project_id FROM tb_zjyc_group_project WHERE project_id = %s", (project_id,))
                if not cursor.fetchone():
                    return error('项目不存在', 404)

                fields = ['project_id', 'user_name']
                values = [project_id, user_name]
                placeholders = ['%s', '%s']

                for field in ['member_type', 'role', 'description']:
                    if field in data:
                        fields.append(field)
                        values.append(data[field])
                        placeholders.append('%s')

                sql = f"INSERT INTO tb_zjyc_group_members ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
                cursor.execute(sql, tuple(values))
                member_id = cursor.lastrowid

        return success({'member_id': member_id}, '成员添加成功')
    except Exception as e:
        return error(f'成员添加失败: {str(e)}', 500)


@project_bp.route('/api/group/<int:project_id>/add-achievement', methods=['POST'])
def add_project_achievement(project_id):
    """9. 添加课题项目成就"""
    try:
        data = request.get_json()
        if not data:
            return error('请求数据不能为空', 400)

        title = data.get('title')
        if not title:
            return error('成就标题不能为空', 400)

        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                fields = ['project_id', 'title']
                values = [project_id, title]
                placeholders = ['%s', '%s']

                for field in ['type', 'description', 'achievement_date', 'status', 'attachment']:
                    if field in data:
                        fields.append(field)
                        values.append(data[field])
                        placeholders.append('%s')

                sql = f"INSERT INTO tb_zjyc_group_achievements ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
                cursor.execute(sql, tuple(values))
                achievement_id = cursor.lastrowid

        return success({'achievement_id': achievement_id}, '成就添加成功')
    except Exception as e:
        return error(f'成就添加失败: {str(e)}', 500)


@project_bp.route('/api/group/statistics', methods=['GET'])
def get_group_statistics():
    """10. 获取课题项目组全局统计"""
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS cnt FROM tb_zjyc_group_project")
                project_cnt = cursor.fetchone()['cnt']

                cursor.execute("SELECT COUNT(*) AS cnt FROM tb_zjyc_group_members")
                member_cnt = cursor.fetchone()['cnt']

                cursor.execute("SELECT COUNT(*) AS cnt FROM tb_zjyc_group_achievements")
                achievement_cnt = cursor.fetchone()['cnt']

                cursor.execute("SELECT type, COUNT(*) AS count FROM tb_zjyc_group_achievements GROUP BY type")
                achievement_by_type = cursor.fetchall()

                cursor.execute("SELECT member_type, COUNT(*) AS count FROM tb_zjyc_group_members GROUP BY member_type")
                member_by_type = cursor.fetchall()

        data = {
            'projectCount': project_cnt,
            'memberCount': member_cnt,
            'achievementCount': achievement_cnt,
            'achievementByType': achievement_by_type,
            'memberByType': member_by_type,
        }
        return success(data, '查询成功')
    except Exception as e:
        return error(f'查询失败: {str(e)}', 500)


@project_bp.route('/api/group/<int:project_id>/toggle-visibility', methods=['PUT'])
def toggle_project_visibility(project_id):
    """11. 切换课题项目显示状态"""
    try:
        data = request.get_json()
        if not data:
            return error('请求数据不能为空', 400)

        is_visible = data.get('is_visible')
        if is_visible is None:
            return error('is_visible 参数不能为空', 400)

        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT project_id FROM tb_zjyc_group_project WHERE project_id = %s", (project_id,))
                if not cursor.fetchone():
                    return error('项目不存在', 404)

                status = 'visible' if is_visible else 'hidden'
                cursor.execute(
                    "UPDATE tb_zjyc_group_project SET status = %s WHERE project_id = %s",
                    (status, project_id)
                )

        return success({
            'project_id': project_id,
            'is_visible': is_visible,
            'status': status,
        }, '项目显示状态已更新')
    except Exception as e:
        return error(f'更新失败: {str(e)}', 500)
