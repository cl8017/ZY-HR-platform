"""
auth 模块 - 本地开发登录（跳过若依SSO）
仅用于开发测试环境，生产环境使用若依认证
"""
import hashlib
import json
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__)

# 开发环境用户表 (仅供测试)
DEV_USERS = {
    'admin': {'password': 'admin123', 'name': '管理员', 'role': 'admin'},
    'zhangsan': {'password': '123456', 'name': '张三', 'role': 'user'},
    'lisi': {'password': '123456', 'name': '李四', 'role': 'user'},
}

# 简单 Token 生成（开发用）
def _make_token(username):
    raw = f"{username}:{datetime.now().timestamp()}:dev-secret"
    return hashlib.md5(raw.encode()).hexdigest()


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """本地登录接口"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'code': 400, 'msg': '请求体不能为空'}), 400

    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'code': 400, 'msg': '用户名和密码不能为空'}), 400

    user = DEV_USERS.get(username)
    if not user or user['password'] != password:
        return jsonify({'code': 401, 'msg': '用户名或密码错误'}), 401

    token = _make_token(username)
    return jsonify({
        'code': 200,
        'msg': '登录成功',
        'token': token,
        'user': {
            'username': username,
            'name': user['name'],
            'role': user['role'],
        }
    })


@auth_bp.route('/auth/info', methods=['GET'])
def user_info():
    """获取当前用户信息"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({'code': 401, 'msg': '未登录'}), 401
    # 开发环境简单验证
    return jsonify({
        'code': 200,
        'user': {
            'username': 'admin',
            'name': '管理员',
            'avatar': '',
            'roles': ['admin'],
        }
    })
