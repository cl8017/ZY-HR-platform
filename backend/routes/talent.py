"""人才库 API — 人才查询、分类统计、评分分析"""

from flask import Blueprint, request
from backend.models.db import db
from backend.utils.helpers import success, error

talent_bp = Blueprint('talent', __name__, url_prefix='/api')


@talent_bp.route('/zjyc/score')
def get_talent_score():
    """人才评分统计"""
    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM v_talent_score")
            data = cursor.fetchall()
    return success(data)


@talent_bp.route('/zjyc/count_by_category')
def count_by_category():
    """人才分类统计"""
    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT category, COUNT(*) AS count
                FROM hs_rencai
                GROUP BY category
                ORDER BY count DESC
            """)
            data = cursor.fetchall()
    return success(data)


@talent_bp.route('/board/talent/category')
def talent_count_by_category():
    """人才数据看板（专业/公司/性别多维统计）"""
    category_filter = request.args.get('category', '')
    category_condition = f"AND r.category = '{category_filter}'" if category_filter else ""

    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            # 专业分类统计
            cursor.execute(f"""
                SELECT er.major_category, COUNT(*) AS major_count
                FROM (SELECT DISTINCT name FROM hs_rencai WHERE 1=1 {category_condition}) r
                LEFT JOIN employee_roster er ON r.name = er.name
                WHERE er.major_category IS NOT NULL
                GROUP BY er.major_category
            """)
            major_stats = cursor.fetchall()

            # 公司分布统计
            cursor.execute(f"""
                SELECT er.company, COUNT(*) AS company_count
                FROM (SELECT DISTINCT name FROM hs_rencai WHERE 1=1 {category_condition}) r
                LEFT JOIN employee_roster er ON r.name = er.name
                WHERE er.company IS NOT NULL
                GROUP BY er.company
            """)
            company_stats = cursor.fetchall()

            # 性别统计
            cursor.execute(f"""
                SELECT er.gender, COUNT(*) AS gender_count
                FROM (SELECT DISTINCT name FROM hs_rencai WHERE 1=1 {category_condition}) r
                LEFT JOIN employee_roster er ON r.name = er.name
                WHERE er.gender IS NOT NULL
                GROUP BY er.gender
            """)
            gender_stats = cursor.fetchall()

    return success({
        'majorStats': major_stats,
        'companyStats': company_stats,
        'genderStats': gender_stats
    })
