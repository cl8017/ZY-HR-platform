"""
通用 CRUD 蓝图 - 若依 Vue 前端标准化 CRUD 接口
自动适配所有 zhenjiang / yancao / system / monitor 等模块
URL 规范:
  GET    /{ns}/{module}/list       - 分页查询列表
  GET    /{ns}/{module}/{id}        - 查询单条
  POST   /{ns}/{module}            - 新增
  PUT    /{ns}/{module}            - 修改
  DELETE /{ns}/{module}/{id}        - 删除
"""
import re
from flask import Blueprint, request, jsonify
from backend.models.db import db_yancao

crud_bp = Blueprint('crud', __name__)

# ── 模块名 → 数据库表名映射 ──────────────────────────
# URL 中的模块名可能与 DB 表名不一致，在此配置
TABLE_MAP = {
    # zhenjiang
    'employee_profile': ('employee_profile', 'id'),
    'competencyAnalysis': ('position_competency_analysis', 'id'),
    'employee_roster': ('employee_roster', 'id'),
    'post': ('hs_post', 'id'),
    'student_roster': ('student_roster', 'id'),
    'profile': ('hs_profile', 'id'),
    'analysis': ('position_competency_analysis', 'id'),
    'monitor': ('talent_dashboard', 'id'),
    'forecast': ('personnel_movement_forecast', 'id'),
    'dept': ('hs_dept', 'dept_id'),
    # yancao
    'rencai': ('hs_rencai', 'id'),
    'requirements': ('hs_requirements', 'id'),
}
# ── 驼峰 ↔ 蛇形 转换 ────────────────────────────────
def _camel_to_snake(name):
    """employeeName → employee_name"""
    s = re.sub(r'([A-Z])', r'_\1', name).lower()
    return s.strip('_')

def _snake_to_camel(name):
    """employee_name → employeeName"""
    parts = name.split('_')
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])

def _fields_to_snake(record):
    """将查询结果的键从蛇形转为驼峰（前端期望蛇形）"""
    if not record:
        return record
    return {_snake_to_camel(k): v for k, v in record.items()}

def _params_to_snake(params):
    """将请求参数的键从驼峰转为蛇形（用于 WHERE）"""
    return {_camel_to_snake(k): v for k, v in params.items()}

# ── 辅助：模块 → 表名 ──────────────────────────────
def _resolve_table(module):
    """返回 (表名, 主键列名)"""
    entry = TABLE_MAP.get(module)
    if entry:
        return entry
    # 如果未映射，直接使用模块名作为表名，默认主键 id
    return (module, 'id')

# ── 列表查询 ───────────────────────────────────────
@crud_bp.route('/<namespace>/<module>/list', methods=['GET'])
def list_records(namespace, module):
    table, pk = _resolve_table(module)
    try:
        page = request.args.get('pageNum', 1, type=int)
        size = request.args.get('pageSize', 10, type=int)
        offset = (page - 1) * size

        # 构建 WHERE 条件（仅用于精确匹配的查询参数）
        conditions = []
        params = []
        for key, val in request.args.items():
            if key in ('pageNum', 'pageSize', 'orderBy', 'order'):
                continue
            if not val:
                continue
            col = _camel_to_snake(key)
            conditions.append(f'`{col}` LIKE %s')
            params.append(f'%{val}%')

        where = 'WHERE ' + ' AND '.join(conditions) if conditions else ''

        with db_yancao.get_conn() as conn:
            with conn.cursor() as cursor:
                # 总数
                cursor.execute(f'SELECT COUNT(*) as cnt FROM `{table}` {where}', params)
                total = cursor.fetchone()['cnt']
                # 分页数据
                cursor.execute(
                    f'SELECT * FROM `{table}` {where} ORDER BY `{pk}` DESC LIMIT %s OFFSET %s',
                    params + [size, offset]
                )
                rows = cursor.fetchall()

        # 转驼峰字段名（前端需要）
        records = [_fields_to_snake(r) for r in rows]

        return jsonify({
            'code': 200,
            'msg': '操作成功',
            'data': {
                'records': records,
                'total': total,
            }
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'code': 500, 'msg': f'查询失败: {str(e)}', 'data': {'records': [], 'total': 0}}), 500

# ── 查询单条 ───────────────────────────────────────
@crud_bp.route('/<namespace>/<module>/<int:record_id>', methods=['GET'])
def get_record(namespace, module, record_id):
    table, pk = _resolve_table(module)
    try:
        with db_yancao.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM `{table}` WHERE `{pk}` = %s', (record_id,))
                row = cursor.fetchone()
        if not row:
            return jsonify({'code': 404, 'msg': '记录不存在'}), 404
        return jsonify({'code': 200, 'msg': '操作成功', 'data': _fields_to_snake(row)})
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

# ── 新增 ───────────────────────────────────────────
@crud_bp.route('/<namespace>/<module>', methods=['POST'])
def create_record(namespace, module):
    table, pk = _resolve_table(module)
    try:
        data = request.get_json(silent=True) or {}
        # 转蛇形字段名
        fields = _params_to_snake(data)
        cols = ', '.join(f'`{k}`' for k in fields.keys())
        placeholders = ', '.join('%s' for _ in fields)
        vals = list(fields.values())

        with db_yancao.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f'INSERT INTO `{table}` ({cols}) VALUES ({placeholders})',
                    vals
                )
                conn.commit()
                new_id = cursor.lastrowid

        return jsonify({'code': 200, 'msg': '操作成功', 'data': {'id': new_id}})
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'新增失败: {str(e)}'}), 500

# ── 修改 ───────────────────────────────────────────
@crud_bp.route('/<namespace>/<module>', methods=['PUT'])
def update_record(namespace, module):
    table, pk = _resolve_table(module)
    try:
        data = request.get_json(silent=True) or {}
        record_id = data.get(pk) or data.get('id')
        if not record_id:
            return jsonify({'code': 400, 'msg': '缺少 id'}), 400

        fields = _params_to_snake(data)
        pk_snake = _camel_to_snake(pk) if pk != 'id' else 'id'
        if pk_snake in fields:
            del fields[pk_snake]
        if 'id' in fields:
            del fields['id']
        if not fields:
            return jsonify({'code': 400, 'msg': '无更新字段'}), 400

        set_clause = ', '.join(f'`{k}` = %s' for k in fields.keys())
        vals = list(fields.values()) + [record_id]

        with db_yancao.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f'UPDATE `{table}` SET {set_clause} WHERE `{pk}` = %s',
                    vals
                )
                conn.commit()

        return jsonify({'code': 200, 'msg': '操作成功', 'data': None})
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'修改失败: {str(e)}'}), 500

# ── 删除 ───────────────────────────────────────────
@crud_bp.route('/<namespace>/<module>/<int:record_id>', methods=['DELETE'])
def delete_record(namespace, module, record_id):
    table, pk = _resolve_table(module)
    try:
        with db_yancao.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'DELETE FROM `{table}` WHERE `{pk}` = %s', (record_id,))
                conn.commit()
        return jsonify({'code': 200, 'msg': '操作成功', 'data': None})
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'删除失败: {str(e)}'}), 500

# ── 批量删除 ───────────────────────────────────────
@crud_bp.route('/<namespace>/<module>/batch', methods=['DELETE'])
def batch_delete(namespace, module):
    table, pk = _resolve_table(module)
    try:
        data = request.get_json(silent=True) or {}
        ids = data.get('ids', [])
        if not ids:
            return jsonify({'code': 400, 'msg': '缺少 ids'}), 400

        placeholders = ', '.join('%s' for _ in ids)
        with db_yancao.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f'DELETE FROM `{table}` WHERE `{pk}` IN ({placeholders})',
                    ids
                )
                conn.commit()
        return jsonify({'code': 200, 'msg': '操作成功', 'data': None})
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'批量删除失败: {str(e)}'}), 500
