"""工具函数 — 统一响应、通用辅助"""

from flask import jsonify


def success(data=None, msg='ok'):
    """统一成功响应"""
    return jsonify({'code': 200, 'msg': msg, 'data': data})


def error(msg='服务器内部错误', code=500, data=None):
    """统一错误响应"""
    return jsonify({'code': code, 'msg': msg, 'data': data}), code


def bad_request(msg='请求参数错误'):
    """400 错误"""
    return error(msg, code=400)


def not_found(msg='资源不存在'):
    """404 错误"""
    return error(msg, code=404)


def paginate(page: int = 1, page_size: int = 20, default_page_size: int = 20):
    """分页参数规范化

    Returns:
        (limit, offset) tuple
    """
    page = max(page, 1)
    page_size = min(max(page_size, 1), 100) or default_page_size
    limit = page_size
    offset = (page - 1) * page_size
    return limit, offset


def camel_case(s: str) -> str:
    """下划线命名转驼峰命名（首字母小写）"""
    if not s:
        return s
    parts = s.split('_')
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])
