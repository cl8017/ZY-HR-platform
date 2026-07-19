"""
dashboard 模块 - 看板/数据统计 API
"""
from flask import Blueprint, request, jsonify
from backend.models.db import db1
from backend.utils.helpers import success, error
from backend.utils.text_utils import camel_case
import json

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/red_alert')
def get_red_alert():
    """查询red_alert表数据"""
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM zy_hr_red_alert")
                data = cursor.fetchall()
        return success(data)
    except Exception as e:
        return error(f'查询失败: {str(e)}', 500)


@dashboard_bp.route('/retirement_personnel_prediction')
def get_retirement_personnel():
    """查询退休预测数据"""
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM zy_hr_retirement_prediction where retiring_count > 0"
                )
                data = cursor.fetchall()
        return success(data)
    except Exception as e:
        return error(f'查询失败: {str(e)}', 500)

@dashboard_bp.route('/position_competency_analysis', methods=['GET'])
def get_position_competency_analysis():
    """查询岗位胜任力分析数据（使用 db2）"""
    from backend.models.db import db2
    try:
        id_val = int(request.args.get('id', 1))
    except ValueError:
        return jsonify({'code': 400, 'msg': '参数id必须为整数'}), 400
    try:
        with db2.get_conn() as conn:
            with conn.cursor() as cursor:
                sql = """
                    SELECT a.*, b.company, b.department 
                    FROM zy_hr_competency_analysis a
                    LEFT JOIN zy_hr_employee_roster b ON a.name = b.name
                    WHERE a.id = %s 
                """
                cursor.execute(sql, (id_val,))
                raw_data = cursor.fetchall()
        formatted_rows = []
        for item in raw_data:
            camel_item = {}
            for key, value in item.items():
                camel_key = camel_case(key)
                camel_item[camel_key] = value
            formatted_rows.append(camel_item)
        result = {
            'code': 200,
            'msg': '查询成功',
            'total': len(formatted_rows),
            'rows': formatted_rows
        }
        return json.dumps(result, ensure_ascii=False, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'查询失败: {str(e)}',
            'total': 0,
            'rows': []
        }), 500
