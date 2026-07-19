"""
统一数据库连接管理
支持 mock 模式（MOCK_DB=1 时返回假数据）
"""
import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from datetime import datetime

from backend.config import config


class DatabaseManager:
    """数据库连接管理器"""

    def __init__(self, db_config, mock_data: dict = None):
        self._config = db_config
        self._mock_data = mock_data or {}

    def _connect(self):
        return pymysql.connect(
            host=self._config.host,
            port=self._config.port,
            user=self._config.user,
            password=self._config.password,
            database=self._config.database,
            charset=self._config.charset,
            connect_timeout=self._config.connect_timeout,
            cursorclass=DictCursor
        )

    @contextmanager
    def get_conn(self):
        """获取数据库连接（上下文管理器，自动提交/回滚）"""
        if config.mock_db:
            yield MockConnection(self._config.database)
            return
        conn = self._connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @contextmanager
    def get_cursor(self):
        """便捷方法：直接获取 cursor"""
        with self.get_conn() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                cursor.close()


class MockConnection:
    """Mock 数据库连接（开发模式无真实数据库时使用）"""

    def __init__(self, db_name='test'):
        self.db_name = db_name

    def cursor(self, cursorclass=None):
        return MockCursor()

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class MockCursor:
    """Mock 游标"""

    def __init__(self):
        self._data = []
        self.lastrowid = 1  # 模拟自增ID

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def execute(self, query, params=None):
        # 根据查询返回不同的假数据
        if 'red_alert' in query:
            self._data = [
                {'id': 1, 'name': '模拟红色预警-张三', 'age': 62, 'department': '营销中心', 'warning_type': 'retirement', 'created_at': datetime.now().isoformat()},
                {'id': 2, 'name': '模拟红色预警-李四', 'age': 57, 'department': '物流中心', 'warning_type': 'retirement', 'created_at': datetime.now().isoformat()},
            ]
        elif 'DUAL' in query or 'UNION ALL' in query:
            # DUAL 联合查询（teacher 路由用）
            self._data = [
                {'name': '张三', 'role': '员工', 'department': '营销中心', 'current_position': '科长'},
                {'name': '李四', 'role': '导师', 'department': '物流中心', 'current_position': '高级工程师'},
            ]
        elif 'retirement' in query.lower():
            self._data = [
                {'id': 1, 'name': '模拟退休预测-张三', 'retiring_count': 3, 'department': '营销中心', 'year': 2026},
                {'id': 2, 'name': '模拟退休预测-李四', 'retiring_count': 1, 'department': '物流中心', 'year': 2027},
            ]
        elif 'personnel_statistics' in query or 'compilation' in query:
            self._data = [
                {'主键ID': 1, '单位名称': '镇江市烟草公司', '部门名称': '营销中心', '人员编制数_总数': 25, '实有人数_总数': 22, '备注': '模拟数据'},
                {'主键ID': 2, '单位名称': '镇江市烟草公司', '部门名称': '物流中心', '人员编制数_总数': 30, '实有人数_总数': 28, '备注': '模拟数据'},
            ]
        elif 'employee_roster' in query:
            self._data = [
                {'员工id': 1, '员工姓名': '模拟张三', 'name': '张三', '员工部门': '营销中心', '当前职位': '科长', '学历': '本科', 'department': '营销中心', 'current_position': '科长'},
                {'员工id': 2, '员工姓名': '模拟李四', 'name': '李四', '员工部门': '物流中心', '当前职位': '副科长', '学历': '硕士', 'department': '物流中心', 'current_position': '副科长'},
            ]
        elif 'employee_profile' in query.lower():
            self._data = [{'name': '张三', 'department': '营销中心', 'current_position': '科长',
                           'technical_certificates': '(2020年)市级：技术认证',
                           'skill_certificates': '(2021年)省级：技能大赛',
                           'municipal_special_projects': '', 'provincial_special_projects': '',
                           'municipal_research_projects': '', 'provincial_research_projects': '',
                           'municipal_competitions': '', 'provincial_competitions': '',
                           'municipal_honors': '', 'provincial_honors': ''}]
        elif 'tb_zjyc_teacher' in query or 'teacher' in query.lower():
            self._data = [
                {'name': '张三', 'role': '员工', 'department': '营销中心', 'current_position': '科长'},
                {'name': '李四', 'role': '导师', 'department': '物流中心', 'current_position': '高级工程师'},
            ]
            # DUAL table queries return a single row
            if 'DUAL' in query:
                self._data = [{'name': '张三', 'role': '员工', 'department': '营销中心', 'current_position': '科长'}]
        elif 'tb_zjyc_score_record' in query or 'score' in query.lower():
            self._data = [
                {'member_name': '张三', 'related_achievement_id': 1, 'before_score': 80, 'after_score': 90,
                 'score_change': 10, 'achievement_type': '论文', 'change_reason': '发表核心期刊',
                 'operate_time': '2026-01-01 10:00:00', 'record_create_time': '2026-01-01 10:00:00'},
            ]
        elif 'hs_rencai' in query or 'talent' in query.lower():
            self._data = [
                {'category': 'admin', 'count': 5, 'total': 20},
                {'category': 'technical', 'count': 8, 'total': 20},
                {'standard_education': '本科', 'person_count': 10},
                {'standard_education': '研究生', 'person_count': 5},
            ]
            # wordcloud query
            if 'wordcloud_tags' in query:
                self._data = [{'wordcloud_tags': '{"wordcloud": [{"name": "技术", "value": 10}, {"name": "管理", "value": 8}]}'}]
        elif 'tb_zjyc_group_project' in query or 'tb_zjyc_group_members' in query or 'group' in query.lower():
            # COUNT 查询优先
            if 'count(*) as cnt' in query.lower() or 'cnt' in query.lower()[:40]:
                self._data = [{'cnt': 5}]
            elif 'count(*) as total' in query.lower():
                self._data = [{'total': 5}]
            elif 'tb_zjyc_group_members' in query:
                self._data = [
                    {'member_id': 1, 'project_id': 1, 'member_name': '张三',
                     'member_title': '负责人', 'member_type': 0, 'sort_order': 1},
                ]
            elif 'tb_zjyc_group_phases' in query:
                self._data = [
                    {'phase_id': 1, 'project_id': 1, 'phase_name': '第一阶段',
                     'phase_description': '调研', 'sort_order': 1},
                ]
            elif 'phase_content' in query.lower():
                self._data = [
                    {'content_id': 1, 'phase_id': 1, 'content_title': '调研报告',
                     'content_text': '已完成调研', 'sort_order': 1},
                ]
            else:
                self._data = [
                    {'project_id': 1, 'project_name': '模拟项目A', 'project_title': '课题研究',
                     'project_description': '模拟课题项目', 'status': 1, 'sort_order': 1,
                     'phase_id': 1, 'member_id': 1, 'achievement_type': '论文',
                     'achievement_title': '成果1', 'achievement_description': '',
                     'achievement_id': 1, 'achievement_icon': '', 'dashboard_id': 1,
                     'dashboard_name': '项目概览', 'dashboard_status': 1},
                ]
        elif 'department' in query and 'retiring' in query:
            self._data = [
                {'department': '营销中心', 'retiring_count': 3, 'total_count': 25, 'retirement_ratio': 12.0, 'is_red_alert': 0},
                {'department': '物流中心', 'retiring_count': 6, 'total_count': 30, 'retirement_ratio': 20.0, 'is_red_alert': 0},
                {'department': '机关科室', 'retiring_count': 12, 'total_count': 28, 'retirement_ratio': 42.86, 'is_red_alert': 1},
            ]
        elif 'position_competency' in query:
            self._data = [{
                'id': 1, 'name': '张三', 'company': '镇江烟草', 'department': '营销中心',
                'score': 85.5, 'level': '优秀', 'analysis_date': '2026-01-01'
            }]
        else:
            self._data = [{'msg': ('mock data for: ' + str(query[:50]))}]
        return len(self._data)

    def fetchall(self):
        return self._data

    def fetchone(self):
        return self._data[0] if self._data else None

    def close(self):
        pass


# 全局实例
db1 = DatabaseManager(config.db1, mock_data={'db_name': 'zj-yancao'})
db2 = DatabaseManager(config.db2, mock_data={'db_name': 'yancao'})
