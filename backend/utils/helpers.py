"""
通用工具函数 - 统一响应格式
"""
from flask import jsonify


def success(data=None, msg='ok'):
    return jsonify({'code': 200, 'msg': msg, 'data': data})


def error(msg='error', code=500):
    return jsonify({'code': code, 'msg': msg, 'data': None}), code
