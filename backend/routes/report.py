"""
report 模块 - 编制/预警/花名册 API
保持原始响应格式，避免前端解析失败
"""
import json
from flask import Blueprint, request, jsonify
from backend.models.db import db1

report_bp = Blueprint('report', __name__)


@report_bp.route('/compilation', methods=['GET'])
def get_compilation():
    """查询personnel_statistics表数据"""
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM zy_hr_personnel_statistics")
                data = cursor.fetchall()
        # 保持原始 json.dumps 格式，确保中文编码
        return json.dumps(data, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return jsonify({'error': f'查询失败: {str(e)}'}), 500

@report_bp.route('/red_alert_department', methods=['GET'])
def get_red_alert_department():
    """根据部门统计退休预警"""
    try:
        male_age = int(request.args.get('male_age', 63))
        female_age = int(request.args.get('female_age', 58))
    except ValueError:
        return jsonify({'error': '参数必须为整数'}), 400
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                sql = """
                SELECT 
                    department, 
                    COUNT(*) AS retiring_count, 
                    (SELECT COUNT(*) FROM zy_hr_employee_roster AS e2 WHERE e2.department = e1.department) AS total_count,
                    ROUND((COUNT(*) / (SELECT COUNT(*) FROM zy_hr_employee_roster AS e2 WHERE e2.department = e1.department)) * 100, 2) AS retirement_ratio,
                    CASE 
                        WHEN COUNT(*) >= (SELECT COUNT(*) * 0.3 FROM zy_hr_employee_roster AS e2 WHERE e2.department = e1.department) THEN 1
                        ELSE 0
                    END AS is_red_alert
                FROM zy_hr_employee_roster AS e1
                WHERE (
                    (gender = '男' AND CAST(SUBSTRING_INDEX(birth_date, '-', 1) AS UNSIGNED) <= YEAR(CURDATE()) - %s)
                    OR 
                    (gender = '女' AND CAST(SUBSTRING_INDEX(birth_date, '-', 1) AS UNSIGNED) <= YEAR(CURDATE()) - %s)
                )
                GROUP BY department;
                """
                cursor.execute(sql, (male_age, female_age))
                data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': f'查询失败: {str(e)}'}), 500


@report_bp.route('/employee_roster_markdown', methods=['GET'])
def get_employee_roster_markdown():
    """分页查询人员花名册"""
    try:
        pagesize = int(request.args.get('pagesize', 1))
        offset = int(request.args.get('offset', 1))
    except ValueError:
        return jsonify({'error': '参数必须为整数'}), 400
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                sql = """
                    SELECT
                        id as '员工id',
                        name as '员工姓名',
                        department as '员工部门',
                        current_position as '当前职位',
                        education_degree as '学历',
                        current_position_years as '当前职位工作时间',
                        major as '专业',
                        political_status as '是否党员',
                        professional_qualification as '专业技术资格',
                        vocational_skill_level as '职业技能等级',
                        work_start_date as '参加工作时间'
                    FROM
                        zy_hr_employee_roster
                    where position_level > 10 and id not in (select id from zy_hr_competency_analysis)
                    ORDER BY CAST(id AS SIGNED) DESC
                    LIMIT %s OFFSET %s;
                """
                cursor.execute(sql, (pagesize, offset))
                data = cursor.fetchall()
        return json.dumps(data, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return jsonify({'error': f'查询失败: {str(e)}'}), 500
