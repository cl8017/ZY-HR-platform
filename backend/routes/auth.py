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


# 验证码开关（开发环境返回固定值）
import base64
import random
import string


@auth_bp.route('/captchaImage', methods=['GET'])
def captcha_image():
    """验证码接口（开发环境返回固定验证码 0000）"""
    import io
    # 生成一个简单的验证码图片（实际返回固定值方便测试）
    captcha_code = '0000'
    
    # 生成一个简单的图片
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (130, 48), (240, 240, 240))
        draw = ImageDraw.Draw(img)
        draw.text((35, 12), captcha_code, fill=(50, 50, 50))
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        img_base64 = base64.b64encode(buf.getvalue()).decode()
    except ImportError:
        img_base64 = ''
    
    return jsonify({
        'code': 200,
        'msg': '操作成功',
        'img': img_base64,
        'captchaEnabled': True,
        'uuid': 'dev-captcha-uuid'
    })


@auth_bp.route('/auth/code', methods=['GET'])
def auth_code():
    """验证码接口（开发环境）"""
    return jsonify({
        'code': 200,
        'msg': '操作成功',
        'data': {
            'img': '',
            'captchaEnabled': False,
            'uuid': 'dev-captcha-uuid',
        }
    })


@auth_bp.route('/auth/tenant/list', methods=['GET'])
def tenant_list():
    """获取租户列表（开发环境关闭租户功能）"""
    return jsonify({
        'code': 200,
        'msg': '操作成功',
        'data': {
            'tenantEnabled': False,
            'voList': [],
        }
    })


@auth_bp.route('/auth/logout', methods=['POST'])
def auth_logout():
    """退出登录"""
    return jsonify({'code': 200, 'msg': '操作成功', 'data': None})


@auth_bp.route('/auth/register', methods=['POST'])
def auth_register():
    """注册（开发环境禁用）"""
    return jsonify({'code': 500, 'msg': '演示环境不支持注册', 'data': None}), 500


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
        'msg': '操作成功',
        'access_token': token,
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
