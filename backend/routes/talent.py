"""
talent 模块 - 人才库 + 大师工作室 API
保持原始响应格式，前端依赖这些字段名
"""
from datetime import datetime

from flask import Blueprint, request, jsonify
from backend.models.db import db1
from backend.utils.helpers import success, error

talent_bp = Blueprint('talent', __name__)


def _format_time(dt):
    """格式化时间对象为字符串"""
    if dt is None:
        return None
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(dt, str):
        return dt
    return str(dt)


@talent_bp.route('/api/zjyc/score', methods=['GET'])
def get_zjyc_score():
    """查 zy_hr_score_record LEFT JOIN zy_hr_member 获取积分变更记录"""
    name = request.args.get('name')
    if not name:
        return error('缺少必填参数 name', 400)

    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                sql = """
                    SELECT
                        s.id,
                        s.achievement_id            AS '关联成果ID',
                        s.before_score              AS '变更前积分',
                        s.after_score               AS '变更后积分',
                        s.score_change              AS '积分变更值',
                        s.achievement_type          AS '关联成果类型',
                        s.change_reason             AS '积分变更原因',
                        s.operation_time            AS '积分操作时间',
                        s.create_time               AS '记录创建时间'
                    FROM zy_hr_score_record s
                    LEFT JOIN zy_hr_member m ON s.member_id = m.id
                    WHERE m.member_name = %s
                    ORDER BY s.create_time DESC
                """
                cursor.execute(sql, (name,))
                rows = cursor.fetchall()

        # 格式化时间字段
        for row in rows:
            if '积分操作时间' in row:
                row['积分操作时间'] = _format_time(row['积分操作时间'])
            if '记录创建时间' in row:
                row['记录创建时间'] = _format_time(row['记录创建时间'])

        return jsonify(rows)
    except Exception as e:
        return error(f'查询积分变更记录失败: {str(e)}', 500)


@talent_bp.route('/api/zjyc/create_master_studio', methods=['POST'])
def create_master_studio():
    """创建大师工作室"""
    data = request.get_json(silent=True)
    if not data:
        return error('请求体不能为空', 400)

    name = data.get('name')
    if not name:
        return error('必填字段 name 不能为空', 400)

    description = data.get('description', '')
    status = data.get('status', 1)
    create_time = data.get('create_time')
    members = data.get('members', [])

    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                insert_sql = """
                    INSERT INTO zy_hr_master_studio (name, description, status, create_time)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_sql, (name, description, status, create_time))
                studio_id = cursor.lastrowid

                # 如果有成员，插入关联表
                if members and isinstance(members, list):
                    member_sql = """
                        INSERT INTO zy_hr_master_studio_member (studio_id, member_id)
                        VALUES (%s, %s)
                    """
                    for member_id in members:
                        cursor.execute(member_sql, (studio_id, member_id))

        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({
            'code': 201,
            'msg': '大师工作室创建成功',
            'data': {
                'studio_id': studio_id,
                'name': name,
                'create_time': create_time or now_str
            }
        }), 201
    except Exception as e:
        return error(f'创建大师工作室失败: {str(e)}', 500)


@talent_bp.route('/api/zjyc/count_by_category', methods=['GET'])
def count_by_category():
    """按类别统计人才去重人数"""
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                sql = """
                    SELECT category, COUNT(DISTINCT name) AS cnt
                    FROM zy_hr_talent_pool
                    WHERE del_flag = '0'
                    GROUP BY category
                """
                cursor.execute(sql)
                rows = cursor.fetchall()

        total = 0
        result = {}
        for row in rows:
            cat = row.get('category', '未知')
            cnt = row.get('cnt', 0)
            result[cat] = cnt
            total += cnt

        result['all'] = total
        return jsonify(result)
    except Exception as e:
        return error(f'统计人才类别失败: {str(e)}', 500)


@talent_bp.route('/api/board/talent/category', methods=['GET'])
def board_talent_category():
    """
    看板-人才类别统计
    支持 cat 过滤 + 额外返回学历分布和年龄分布
    """
    cat = request.args.get('cat')

    # category 映射（原始代码使用字符串拼接构建过滤条件）
    category_map = {
        'admin': '行政管理类',
        'innovation': '科技创新类',
        'teacher': '技能大师类',
        'technical': '专业技术类',
    }

    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                # --- 1) 类别统计 ---
                if cat and cat in category_map:
                    category_filter = "AND category = %s"
                    cat_params = [category_map[cat]]
                else:
                    category_filter = ""
                    cat_params = []

                count_sql = f"""
                    SELECT category, COUNT(DISTINCT name) AS cnt
                    FROM zy_hr_talent_pool
                    WHERE del_flag = '0' {category_filter}
                    GROUP BY category
                """
                cursor.execute(count_sql, cat_params)
                category_rows = cursor.fetchall()

                total = 0
                category_counts = {}
                for row in category_rows:
                    c = row.get('category', '未知')
                    cnt = row.get('cnt', 0)
                    category_counts[c] = cnt
                    total += cnt
                category_counts['all'] = total

                # --- 2) 学历分布 ---
                edu_sql = f"""
                    SELECT education, COUNT(DISTINCT name) AS cnt
                    FROM zy_hr_talent_pool
                    WHERE del_flag = '0' {category_filter}
                    GROUP BY education
                """
                cursor.execute(edu_sql, cat_params)
                edu_rows = cursor.fetchall()
                education_distribution = {}
                for row in edu_rows:
                    edu = row.get('education', '未知')
                    cnt = row.get('cnt', 0)
                    education_distribution[edu] = cnt

                # --- 3) 年龄分布 (暂跳过，talent_pool 无 birth_date 字段) ---
                age_distribution = {}

        # 不需要 age 字段时只返回前端的格式
        result = {
            'category_counts': category_counts,
            'education_distribution': education_distribution,
            'age_distribution': age_distribution,
        }
        return jsonify(result)
    except Exception as e:
        return error(f'查询人才看板失败: {str(e)}', 500)
