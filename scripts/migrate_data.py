#!/usr/bin/env python3
"""Migrate data from yancao (old tables) to zy_hr (new zy_hr_ tables)"""
import pymysql
from datetime import datetime, date
from decimal import Decimal
import sys

SRC = dict(host='127.0.0.1', port=3306, user='root', password='112233', database='yancao')
DST = dict(host='127.0.0.1', port=3306, user='root', password='112233', database='zy_hr')

def escape(val):
    if val is None:
        return "NULL"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, Decimal):
        return str(val)
    if isinstance(val, (datetime, date)):
        return f"'{val.isoformat()}'"
    s = str(val).replace("\\", "\\\\").replace("'", "\\'")
    return f"'{s}'"

# Table mapping with column adjustments
MIGRATIONS = [
    # (source_table, dest_table, column_map)
    # column_map: dict of {dest_col: source_col} or {dest_col: (source_col, default_value)}
    ('employee_roster', 'zy_hr_employee_roster', None),  # auto-map by matching names
    ('employee_profile', 'zy_hr_employee_profile', None),
    ('red_alert', 'zy_hr_red_alert', None),
    ('retirement_personnel_prediction', 'zy_hr_retirement_prediction', None),
    ('personnel_statistics', 'zy_hr_personnel_statistics', None),
    ('position_competency_analysis', 'zy_hr_competency_analysis', None),
    ('hs_rencai', 'zy_hr_talent_pool', None),
    ('tb_zjyc_teacher', 'zy_hr_teacher', None),
    ('tb_zjyc_score_record', 'zy_hr_score_record', None),
    ('tb_zjyc_member', 'zy_hr_member', None),
    ('tb_zjyc_masterstudio_info', 'zy_hr_master_studio', None),
    ('tb_zjyc_masterstudio_member', 'zy_hr_master_studio_member', None),
    ('tb_zjyc_group_project', 'zy_hr_group_project', None),
    ('tb_zjyc_group_members', 'zy_hr_group_members', None),
    ('tb_zjyc_group_phases', 'zy_hr_group_phases', None),
    ('tb_zjyc_group_phase_content', 'zy_hr_group_phase_content', None),
    ('tb_zjyc_group_achievements', 'zy_hr_group_achievements', None),
    ('tb_zjyc_group_dashboards', 'zy_hr_group_dashboards', None),
]

src = pymysql.connect(**SRC)
dst = pymysql.connect(**DST)
scur = src.cursor()
dcur = dst.cursor()

total_ok = 0
total_err = 0

for src_table, dst_table, col_map in MIGRATIONS:
    # Get columns for source and dest
    scur.execute(f"SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='yancao' AND TABLE_NAME='{src_table}' ORDER BY ORDINAL_POSITION")
    src_cols = [r[0] for r in scur.fetchall()]
    
    dcur.execute(f"SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='zy_hr' AND TABLE_NAME='{dst_table}' ORDER BY ORDINAL_POSITION")
    dst_cols = [r[0] for r in dcur.fetchall()]
    
    # Find intersection (columns that exist in both)
    src_set = set(src_cols)
    common_cols = [c for c in dst_cols if c in src_set and c not in ('id',)]
    
    if not common_cols:
        print(f"  Skipping {src_table} -> {dst_table}: no common columns")
        continue
    
    # Read from source
    col_str = ', '.join([f'`{c}`' for c in common_cols])
    scur.execute(f"SELECT {col_str} FROM `{src_table}`")
    rows = scur.fetchall()
    
    if not rows:
        print(f"  {src_table:40s} -> {dst_table:40s}  0 rows (empty)")
        continue
    
    # Clear dest table
    dcur.execute(f"SET FOREIGN_KEY_CHECKS = 0")
    dcur.execute(f"TRUNCATE TABLE `{dst_table}`")
    dcur.execute(f"SET FOREIGN_KEY_CHECKS = 1")
    
    # Insert into dest
    placeholders = ', '.join(['%s'] * len(common_cols))
    insert_cols = ', '.join([f'`{c}`' for c in common_cols])
    
    ok = 0
    err = 0
    for row in rows:
        try:
            dcur.execute(f"INSERT INTO `{dst_table}` ({insert_cols}) VALUES ({placeholders})", row)
            ok += 1
        except Exception as e:
            err += 1
            if err <= 3:
                print(f"    Error: {str(e)[:60]}")
    
    dst.commit()
    print(f"  {src_table:40s} -> {dst_table:40s}  {ok+err} rows ({ok} OK, {err} errors)")
    total_ok += ok
    total_err += err

src.close()
dst.close()
print(f"\nTotal: {total_ok} rows migrated, {total_err} errors")
