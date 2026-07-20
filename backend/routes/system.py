"""
system 模块 - 系统管理 API（菜单/用户/角色）
从 RuoYi sys_* 表读取数据，提供前端导航和权限的接口
"""
from flask import Blueprint, jsonify, request
from backend.models.db import db_yancao

system_bp = Blueprint('system', __name__)


def _derive_route_name(path, component=None, seen_names=None):
    """从组件路径推导 Vue 路由 name（PascalCase），自动去重
    例: yancao/rencai/index → Rencai,   system/user/index → User
    重复会在末尾加 _2, _3 ... 确保唯一
    """
    raw = component or path or ''
    raw = raw.replace('.vue', '').replace('.html', '')
    parts = [p for p in raw.replace('\\', '/').split('/') if p and p not in ('index', 'Index')]
    last = parts[-1] if parts else raw
    base = ''.join(w[0].upper() + w[1:] for w in last.replace('-', '_').split('_') if w)
    if not base:
        base = 'Route'
    # 去重
    if seen_names is not None:
        name = base
        counter = 2
        while name in seen_names:
            name = f'{base}_{counter}'
            counter += 1
        seen_names.add(name)
        return name
    return base


def _normalize_path(path):
    """确保路径以 / 开头"""
    path = path or ''
    if path and not path.startswith('/'):
        path = '/' + path
    return path


def _build_menu_tree(items, parent_id=0, seen_names=None):
    """将扁平菜单列表构建为树形结构（若依 Vue 前端路由格式）"""
    if seen_names is None:
        seen_names = set()
    children = []
    for item in items:
        if item.get('parent_id') == parent_id or (parent_id == 0 and item.get('parent_id') is None):
            sub = _build_menu_tree(items, item['menu_id'], seen_names)
            component = item.get('component') or ''
            path_raw = item.get('path') or ''
            path = _normalize_path(path_raw)
            node = {
                'id': item['menu_id'],
                'label': item['menu_name'],
                'name': _derive_route_name(path, component, seen_names),
                'icon': item.get('icon') or '',
                'path': path,
                'component': component,
                'type': item.get('menu_type', 'M'),
                'visible': item.get('visible') == '0',
                'order': item.get('order_num', 0),
                'children': sub,
            }
            children.append(node)
    children.sort(key=lambda x: x['order'])
    return children


@system_bp.route('/system/dict/data/type/<string:dict_type>', methods=['GET'])
def get_dict_data(dict_type):
    """获取字典数据"""
    try:
        with db_yancao.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT dict_value, dict_label, dict_type, css_class, list_class, is_default, status, remark
                    FROM sys_dict_data WHERE dict_type = %s AND status = '0' ORDER BY dict_sort
                """, (dict_type,))
                data = cursor.fetchall()
        return jsonify({'code': 200, 'msg': '操作成功', 'data': data})
    except Exception as e:
        return jsonify({'code': 200, 'msg': '操作成功', 'data': []})


@system_bp.route('/system/config/configKey/<string:config_key>', methods=['GET'])
def get_config_key(config_key):
    """获取参数配置"""
    try:
        with db_yancao.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT config_value, config_key FROM sys_config WHERE config_key = %s", (config_key,))
                row = cursor.fetchone()
        return jsonify({'code': 200, 'msg': '操作成功', 'data': row or {}})
    except Exception as e:
        return jsonify({'code': 200, 'msg': '操作成功', 'data': {}})


@system_bp.route('/system/dict/type/optionselect', methods=['GET'])
def dict_type_optionselect():
    """获取字典类型选项"""
    try:
        with db_yancao.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT dict_id, dict_type, dict_name FROM sys_dict_type WHERE status = '0'")
                data = cursor.fetchall()
        return jsonify({'code': 200, 'msg': '操作成功', 'data': data})
    except Exception as e:
        return jsonify({'code': 200, 'msg': '操作成功', 'data': []})


@system_bp.route('/system/user/profile', methods=['GET'])
def user_profile():
    """获取用户个人信息"""
    return get_user_info_ruoyi()


@system_bp.route('/system/menu/treeselect', methods=['GET'])
def menu_treeselect():
    """获取菜单树选择"""
    return get_menu_tree()


@system_bp.route('/system/menu/list', methods=['GET'])
def menu_list():
    """获取菜单列表"""
    try:
        with db_yancao.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT menu_id, parent_id, menu_name, path, component, menu_type,
                           visible, status, perms, order_num, icon, create_time
                    FROM sys_menu ORDER BY parent_id, order_num
                """)
                data = cursor.fetchall()
        return jsonify({'code': 200, 'msg': '操作成功', 'data': data})
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500


@system_bp.route('/system/menu/getRouters', methods=['GET'])
def get_routers():
    """获取路由（若依Vue前端调用）"""
    return get_menu_tree()


@system_bp.route('/system/user/getInfo', methods=['GET'])
def get_user_info_ruoyi():
    """获取用户信息（若依Vue前端调用）"""
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
                cursor.execute("""
                    SELECT r.role_id, r.role_name, r.role_key
                    FROM sys_user_role ur
                    JOIN sys_role r ON ur.role_id = r.role_id
                    WHERE ur.user_id = %s
                """, (user['user_id'],))
                roles = cursor.fetchall()
        return jsonify({
            'code': 200, 'msg': '操作成功',
            'data': {
                'user': {
                    'userId': user['user_id'], 'userName': user['user_name'],
                    'nickName': user['nick_name'], 'deptName': user.get('dept_name', ''),
                    'email': user['email'], 'phonenumber': user['phonenumber'],
                    'sex': user['sex'], 'avatar': user['avatar'],
                },
                'roles': [r['role_key'] for r in roles] or ['admin'],
                'permissions': ['*:*:*'],
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500


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
            'msg': '操作成功',
            'data': {
                'user': {
                    'userId': user['user_id'],
                    'userName': user['user_name'],
                    'nickName': user['nick_name'],
                    'deptName': user.get('dept_name', ''),
                    'email': user['email'],
                    'phonenumber': user['phonenumber'],
                    'sex': user['sex'],
                    'avatar': user['avatar'],
                },
                'roles': [r['role_key'] for r in roles] or ['admin'],
                'permissions': ['*:*:*'],
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'查询用户失败: {str(e)}'}), 500
