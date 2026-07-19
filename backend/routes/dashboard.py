"""
dashboard 模块 - 看板/数据统计 API
"""
from flask import Blueprint, request
from backend.models.db import db1
from backend.utils.helpers import success, error

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/red_alert')
def get_red_alert():
    """查询red_alert表数据"""
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM red_alert")
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
                    "SELECT * FROM Retirement_personnel_prediction where retiring_count > 0"
                )
                data = cursor.fetchall()
        return success(data)
    except Exception as e:
        return error(f'查询失败: {str(e)}', 500)
