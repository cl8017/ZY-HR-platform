"""
system 模块 - 系统管理 API（菜单/用户/角色）
从 RuoYi sys_* 表读取数据，提供前端导航和权限的接口
"""
from flask import Blueprint, jsonify, request
from backend.models.db import db_yancao

system_bp = Blueprint('system', __name__)


def _build_menu_tree(items, parent_id=0):
    """将扁平菜单列表构建为树形结构"""
    children = []
    for item in items:
        if item.get('parent_id') == parent_id or (parent_id == 0 and item.get('parent_id') is None):
            sub = _build_menu_tree(items, item['menu_id'])
            node = {
                'id': item['menu_id'],
                'label': item['menu_name'],
                'icon': item.get('icon') or '',
                'path': item.get('path') or '',
                'type': item.get('menu_type', 'M'),
                'visible': item.get('visible') == '0',
                'order': item.get('order_num', 0),
                'children': sub,
            }
            children.append(node)
    children.sort(key=lambda x: x['order'])
    return children


@system_bp.route('/sys/menu/tree', methods=['GET'])
def get_menu_tree():
    """获取菜单树（前端导航用）"""
    try:
        with db_yancao.get_conn() as conn:
            with conn.cursor() as cursor:
                # 从 yancao.sys_menu 获取数据
                cursor.execute("""
                    SELECT menu_id, parent_id, menu_name, path, component,
                           menu_type, visible, status, perms, order_num, icon
                    FROM sys_menu
                    WHERE status = '0' AND menu_type IN ('M', 'C')
                    ORDER BY parent_id, order_num
                """)
                rows = cursor.fetchall()
        tree = _build_menu_tree(rows)
        return jsonify({'code': 200, 'data': tree, 'msg': 'ok'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'查询菜单失败: {str(e)}', 'data': []}), 500


@system_bp.route('/sys/user/info', methods=['GET'])
def get_user_info():
    """获取当前用户信息"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({'code': 401, 'msg': '未登录'}), 401
    # 开发环境返回默认用户
    try:
        with db_yancao.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT u.user_id, u.user_name, u.nick_name, u.dept_id,
                           u.email, u.phonenumber, u.sex, u.status,
                           u.avatar, d.dept_name
                    FROM sys_user u
                    LEFT JOIN sys_dept d ON u.dept_id = d.dept_id
                    LIMIT 1
                """)
                user = cursor.fetchone()
                if not user:
                    return jsonify({'code': 404, 'msg': '用户不存在'}), 404
                # 获取角色
                cursor.execute("""
                    SELECT r.role_id, r.role_name, r.role_key
                    FROM sys_user_role ur
                    JOIN sys_role r ON ur.role_id = r.role_id
                    WHERE ur.user_id = %s
                """, (user['user_id'],))
                roles = cursor.fetchall()
        return jsonify({
            'code': 200,
            'user': {
                'userId': user['user_id'],
                'userName': user['user_name'],
                'nickName': user['nick_name'],
                'deptName': user.get('dept_name', ''),
                'email': user['email'],
                'phone': user['phonenumber'],
                'sex': user['sex'],
                'avatar': user['avatar'],
                'roles': [r['role_key'] for r in roles] or ['admin'],
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'查询用户失败: {str(e)}'}), 500
