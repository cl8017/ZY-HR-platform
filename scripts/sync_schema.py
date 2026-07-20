#!/usr/bin/env python3
"""
ZY-HR 数据库 Schema 版本管理脚本
检测并同步表结构到最新版本
"""
import os
import sys
import pymysql

# 数据库配置（优先级: 环境变量 > .env > 默认）
DB_CONFIG = {
    'host': os.getenv('DB_HOST', os.getenv('DB2_HOST', '127.0.0.1')),
    'port': int(os.getenv('DB_PORT', os.getenv('DB2_PORT', '3306'))),
    'user': os.getenv('DB_USER', os.getenv('DB2_USER', 'root')),
    'password': os.getenv('DB_PASSWORD', os.getenv('DB2_PASSWORD', '112233')),
    'database': 'zy_hr',
}

SCHEMA_VERSION = '0.3.0'

# 期望的表结构清单（表名 → 最少期望的列数）
EXPECTED_TABLES = {
    'zy_hr_employee_roster': 34,
    'zy_hr_employee_profile': 16,
    'zy_hr_red_alert': 11,
    'zy_hr_retirement_prediction': 10,
    'zy_hr_personnel_statistics': 27,
    'zy_hr_competency_analysis': 22,
    'zy_hr_talent_pool': 21,
    'zy_hr_teacher': 10,
    'zy_hr_score_record': 10,
    'zy_hr_member': 7,
    'zy_hr_master_studio': 6,
    'zy_hr_master_studio_member': 6,
    'zy_hr_group_project': 16,
    'zy_hr_group_members': 8,
    'zy_hr_group_phases': 8,
    'zy_hr_group_phase_content': 7,
    'zy_hr_group_achievements': 11,
    'zy_hr_group_dashboards': 10,
}


def check_database():
    """检查数据库状态并返回报告"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cur = conn.cursor()
    except pymysql.err.OperationalError as e:
        return {'status': 'error', 'msg': f'无法连接数据库: {e}'}

    report = {'status': 'ok', 'version': SCHEMA_VERSION, 'tables': {}}

    # 检查每张表
    for table, expected_cols in EXPECTED_TABLES.items():
        try:
            cur.execute(f"SELECT COUNT(*) FROM information_schema.COLUMNS "
                       f"WHERE TABLE_SCHEMA='zy_hr' AND TABLE_NAME='{table}'")
            actual_cols = cur.fetchone()[0]
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = cur.fetchone()[0]
            status = 'ok' if actual_cols >= expected_cols else 'missing_columns'
            report['tables'][table] = {
                'status': status,
                'columns': actual_cols,
                'expected': expected_cols,
                'rows': row_count,
            }
        except pymysql.err.ProgrammingError:
            report['tables'][table] = {
                'status': 'missing',
                'columns': 0,
                'expected': expected_cols,
                'rows': 0,
            }

    conn.close()
    return report


def print_report(report):
    """打印检查报告"""
    if report['status'] == 'error':
        print(f"❌ {report['msg']}")
        return

    print(f"\n📊 ZY-HR Schema 版本: {report['version']}")
    print(f"{'='*60}")
    print(f"{'表名':40s} {'列数':>5s} {'期望':>5s} {'行数':>6s}  状态")
    print(f"{'-'*60}")
    ok = 0
    for name, info in sorted(report['tables'].items()):
        status_icon = {
            'ok': '✅',
            'missing_columns': '⚠️',
            'missing': '❌',
        }.get(info['status'], '❓')
        s = f"{name:40s} {info['columns']:>5d} {info['expected']:>5d} {info['rows']:>6d}  {status_icon}"
        print(s)
        if info['status'] == 'ok':
            ok += 1
    print(f"{'='*60}")
    print(f"共 {len(report['tables'])} 张表, {ok} 张正常, {len(report['tables'])-ok} 张异常")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ZY-HR 数据库 Schema 管理')
    parser.add_argument('action', nargs='?', default='check',
                       choices=['check', 'repair', 'init'],
                       help='操作: check(检查), repair(修复), init(初始化)')
    args = parser.parse_args()

    if args.action == 'check':
        report = check_database()
        print_report(report)
        if any(t['status'] != 'ok' for t in report.get('tables', {}).values()):
            sys.exit(1)
    elif args.action == 'repair':
        print("执行修复...")
        # 读取并执行 schema_alter.sql
        sql_path = os.path.join(os.path.dirname(__file__), 'schema_alter.sql')
        if not os.path.exists(sql_path):
            print(f"❌ 找不到 {sql_path}")
            sys.exit(1)
        with open(sql_path) as f:
            sql = f.read()
        conn = pymysql.connect(**{**DB_CONFIG, 'database': 'zy_hr'})
        cur = conn.cursor()
        ok = 0
        for stmt in sql.split(';'):
            stmt = stmt.strip()
            if not stmt or stmt.startswith('--'):
                continue
            try:
                cur.execute(stmt)
                ok += 1
            except Exception as e:
                if 'Duplicate column' not in str(e):
                    print(f"  ⚠️ {str(e)[:60]}")
        conn.commit()
        conn.close()
        print(f"✅ 执行了 {ok} 条 SQL 语句")
    elif args.action == 'init':
        print("初始化数据库...")
        # 读取 schema.sql
        sql_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if not os.path.exists(sql_path):
            print(f"❌ 找不到 {sql_path}")
            sys.exit(1)
        with open(sql_path) as f:
            sql = f.read()
        conn = pymysql.connect(**{**DB_CONFIG, 'database': None})
        cur = conn.cursor()
        cur.execute("DROP DATABASE IF EXISTS zy_hr")
        cur.execute("CREATE DATABASE zy_hr DEFAULT CHARSET utf8mb4")
        conn.commit()
        conn.close()
        # 再连 zy_hr 执行建表
        conn = pymysql.connect(**{**DB_CONFIG, 'database': 'zy_hr'})
        cur = conn.cursor()
        ok = 0
        for stmt in sql.split(';'):
            stmt = stmt.strip()
            if not stmt or stmt.startswith('--') or stmt.startswith('#'):
                continue
            try:
                cur.execute(stmt)
                ok += 1
            except Exception as e:
                print(f"  ⚠️ {str(e)[:60]}")
        conn.commit()
        conn.close()
        print(f"✅ 初始化完成: {ok} 条语句")
