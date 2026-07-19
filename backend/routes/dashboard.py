"""数据看板 API — 红色预警、退休预测、编制统计、岗位胜任力"""

from flask import Blueprint, request
from backend.models.db import db
from backend.utils.helpers import success, error, bad_request

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='')


@dashboard_bp.route('/red_alert')
def get_red_alert():
    """红色预警数据"""
    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM red_alert")
            data = cursor.fetchall()
    return success(data)


@dashboard_bp.route('/retirement_personnel_prediction')
def get_retirement_personnel():
    """退休人员预测"""
    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM Retirement_personnel_prediction WHERE retiring_count > 0"
            )
            data = cursor.fetchall()
    return success(data)


@dashboard_bp.route('/compilation')
def get_compilation():
    """人员编制统计"""
    from flask import json as flask_json
    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id AS '主键ID',
                    unit AS '单位名称',
                    department AS '部门名称',
                    authorized_total AS '人员编制数_总数',
                    authorized_unit_leader AS '人员编制数_单位（非）领导职数',
                    authorized_department_leader AS '人员编制数_部门领导',
                    authorized_secondary_dept_head AS '人员编制数_二级部门负责人',
                    authorized_section_level_non_leader AS '人员编制数_科级非领导职务',
                    authorized_clerk_level12 AS '人员编制数_一、二级科员',
                    authorized_comprehensive_affairs AS '人员编制数_综合事务类',
                    authorized_business_operation AS '人员编制数_业务及生产操作类岗位',
                    actual_total AS '实有人数_总数',
                    actual_unit_leader AS '实有人数_单位（非）领导职数',
                    actual_department_leader AS '实有人数_部门领导',
                    actual_secondary_dept_head AS '实有人数_二级部门负责人',
                    actual_section_level_non_leader AS '实有人数_科级非领导职务',
                    actual_clerk_level12 AS '实有人数_一、二级科员',
                    actual_comprehensive_affairs AS '实有人数_综合事务类',
                    actual_business_operation AS '实有人数_业务及生产操作类岗位',
                    remark AS '备注'
                FROM personnel_statistics
            """)
            data = cursor.fetchall()
    return flask_json.jsonify(data), 200, {'Content-Type': 'application/json; charset=utf-8'}


@dashboard_bp.route('/red_alert_department')
def get_red_alert_department():
    """部门预警分析"""
    male_age = request.args.get('male_age', 63, type=int)
    female_age = request.args.get('female_age', 58, type=int)

    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            sql = """
                SELECT
                    department,
                    COUNT(*) AS retiring_count,
                    (SELECT COUNT(*) FROM employee_roster AS e2 WHERE e2.department = e1.department) AS total_count,
                    ROUND((COUNT(*) / (SELECT COUNT(*) FROM employee_roster AS e2 WHERE e2.department = e1.department)) * 100, 2) AS retirement_ratio,
                    CASE
                        WHEN COUNT(*) >= (SELECT COUNT(*) * 0.3 FROM employee_roster AS e2 WHERE e2.department = e1.department) THEN 1
                        ELSE 0
                    END AS is_red_alert
                FROM employee_roster AS e1
                WHERE (
                    (gender = '男' AND CAST(SUBSTRING_INDEX(birth_date, '-', 1) AS UNSIGNED) <= YEAR(CURDATE()) - %s)
                    OR
                    (gender = '女' AND CAST(SUBSTRING_INDEX(birth_date, '-', 1) AS UNSIGNED) <= YEAR(CURDATE()) - %s)
                )
                GROUP BY department
            """
            cursor.execute(sql, (male_age, female_age))
            data = cursor.fetchall()
    return success(data)


@dashboard_bp.route('/employee_roster_markdown')
def get_employee_roster_markdown():
    """员工花名册"""
    from flask import json as flask_json
    page_size = request.args.get('pagesize', 1, type=int)
    offset = request.args.get('offset', 1, type=int)

    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            sql = """
                SELECT
                    id as '员工ID',
                    name as '姓名',
                    department as '员工部门',
                    current_position as '当前职位',
                    education_degree as '学历',
                    current_position_years as '当前职位工作时间',
                    major as '专业',
                    political_status as '是否党员',
                    professional_qualification as '专业技术资格',
                    vocational_skill_level as '职业技能等级',
                    work_start_date as '参加工作时间'
                FROM employee_roster
                WHERE position_level > 10
                  AND id NOT IN (SELECT id FROM position_competency_analysis)
                ORDER BY CAST(id AS SIGNED) DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (page_size, offset - 1))
            data = cursor.fetchall()
    return flask_json.jsonify(data), 200, {'Content-Type': 'application/json; charset=utf-8'}


@dashboard_bp.route('/position_competency_analysis')
def get_position_competency_analysis():
    """岗位胜任力分析"""
    emp_id = request.args.get('id', 1, type=int)

    with db.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, name,
                       COALESCE(competency_score1, 0) as score1,
                       COALESCE(competency_score2, 0) as score2,
                       COALESCE(competency_score3, 0) as score3,
                       COALESCE(competency_score4, 0) as score4,
                       COALESCE(competency_score5, 0) as score5
                FROM position_competency_analysis
                WHERE id = %s
            """, (emp_id,))
            data = cursor.fetchone()

    if not data:
        return error(f'未找到ID为{emp_id}的员工胜任力数据', 404)
    return success(data)


@dashboard_bp.route('/api/health')
def health_check():
    """健康检查"""
    db_ok = db.test_connection()
    return success({
        'status': 'running',
        'db': 'ok' if db_ok else 'error',
        'version': '2.0.0'
    })
