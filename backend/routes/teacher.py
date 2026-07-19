"""
teacher 模块 - 导师帮带 API
迁移自 zjyc_api.py L527-656
"""
import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from backend.models.db import db1
from backend.utils.text_utils import preprocess_chinese_text, parse_event_field

teacher_bp = Blueprint('teacher', __name__)


def _get_employee_events(name):
    """根据姓名查询员工事件"""
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                processed_name = preprocess_chinese_text(name)
                cursor.execute(
                    "SELECT * FROM employee_profile WHERE name LIKE %s",
                    (f'%{processed_name}%',)
                )
                employee = cursor.fetchone()

        if not employee:
            return None, "未找到该员工信息"

        events = []
        field_mappings = [
            ('technical_certificates', 'technical_certificate'),
            ('skill_certificates', 'skill_certificate'),
            ('municipal_special_projects', 'municipal_special'),
            ('provincial_special_projects', 'provincial_special'),
            ('municipal_research_projects', 'municipal_research'),
            ('provincial_research_projects', 'provincial_research'),
            ('municipal_competitions', 'municipal_competition'),
            ('provincial_competitions', 'provincial_competition'),
            ('municipal_honors', 'municipal_honor'),
            ('provincial_honors', 'provincial_honor'),
        ]
        for field, etype in field_mappings:
            events.extend(parse_event_field(employee.get(field), etype))

        events.sort(key=lambda x: x['date'])

        years = sorted({e['date'].split('-')[0] for e in events})
        if not years:
            current_year = datetime.now().year
            years = [str(current_year - 2), str(current_year - 1), str(current_year)]

        labels = []
        for year in years:
            labels.append(f"{year}-01")
            labels.append(f"{year}-07")

        data = []
        base_score = 70
        for idx, label in enumerate(labels):
            year = label.split('-')[0]
            high_level_count = sum(
                1 for event in events
                if event['date'].split('-')[0] <= year
                and event['event'].startswith('省级及以上')
            )
            score = base_score + idx * 1 + high_level_count * 2
            data.append(min(score, 95))

        result = {
            "scores": {
                "labels": labels,
                "datasets": [{
                    "label": "技能评分",
                    "data": data,
                    "borderColor": "#0EA5E9",
                    "backgroundColor": "rgba(14, 165, 233, 0.1)",
                    "tension": 0.4,
                    "fill": True
                }]
            },
            "events": events
        }
        return result, None

    except Exception as e:
        return None, f"查询出错: {str(e)}"


def _get_person_wordcloud(name):
    """根据姓名查询人员词云数据"""
    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                processed_name = preprocess_chinese_text(name)
                cursor.execute(
                    "SELECT wordcloud_tags FROM hs_rencai WHERE name = %s",
                    (processed_name,)
                )
                result = cursor.fetchone()

        if not result:
            return None, "未找到该人员的词云数据"

        wordcloud_data = json.loads(result['wordcloud_tags'])
        return wordcloud_data.get('wordcloud', []), None

    except json.JSONDecodeError as e:
        return None, "词云数据格式错误"
    except Exception as e:
        return None, f"查询出错: {str(e)}"


def _format_time(time_value):
    """格式化时间为 xxxx-xx-xx hh:mm:ss 格式"""
    import re
    if not time_value:
        return ""
    if isinstance(time_value, datetime):
        return time_value.strftime("%Y-%m-%d %H:%M:%S")
    time_str = str(time_value).strip()
    if not time_str:
        return ""
    try:
        if "GMT" in time_str:
            dt = datetime.strptime(time_str, "%a, %d %b %Y %H:%M:%S GMT")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        if re.match(r"\d{4}[-/]\d{2}[-/]\d{2}", time_str):
            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S",
                         "%Y/%m/%d %H:%M:%S", "%Y-%m-%d"]:
                try:
                    dt = datetime.strptime(time_str.split('.')[0], fmt)
                    return dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue
        dt = datetime.strptime(time_str.split('.')[0], "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return time_str


@teacher_bp.route('/employee/events', methods=['GET'])
def employee_events():
    """根据姓名查询员工事件接口"""
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "请提供员工姓名"}), 400

    result, error = _get_employee_events(name)
    if error:
        return jsonify({"error": error}), 500 if "未找到" not in error else 404
    return jsonify(result)


@teacher_bp.route('/person/wordcloud', methods=['GET'])
def person_wordcloud():
    """获取人员词云数据接口"""
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "请提供人员姓名"}), 400

    wordcloud_data, error = _get_person_wordcloud(name)
    if error:
        status = 404 if "未找到" in error else 500
        return jsonify({"error": error}), status
    return jsonify(wordcloud_data)


@teacher_bp.route('/api/zjyc/teacher', methods=['GET'])
def get_related_people():
    """根据姓名查询相关人员信息接口"""
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "请提供姓名参数"}), 400

    try:
        with db1.get_conn() as conn:
            with conn.cursor() as cursor:
                processed_name = preprocess_chinese_text(name)
                sql = """
                select a.name, a.role, b.department, b.current_position from
                (select %s as name, '员工' as role from DUAL
                union all
                select teacher, type from tb_zjyc_teacher where name = %s) a
                left join employee_roster b on a.name = b.name
                """
                cursor.execute(sql, (processed_name, processed_name))
                results = cursor.fetchall()

        avatar_ids = [1005, 1012, 1025, 1074, 1027, 1066, 1072]
        related_people = []
        for idx, item in enumerate(results):
            avatar_id = avatar_ids[idx % len(avatar_ids)]
            related_people.append({
                "id": idx + 1,
                "name": item['name'] or "",
                "department": item['department'] or "",
                "role": item['role'] or "",
                "avatar": f"http://210.16.170.156:58000/static/img/{item['name']}.jpg"
            })
        return jsonify(related_people)

    except Exception as e:
        return jsonify({"error": f"查询出错: {str(e)}"}), 500
