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
        elif 'retirement' in query.lower():
            self._data = [
                {'id': 1, 'name': '模拟退休预测-张三', 'retiring_count': 3, 'department': '营销中心', 'year': 2026},
                {'id': 2, 'name': '模拟退休预测-李四', 'retiring_count': 1, 'department': '物流中心', 'year': 2027},
            ]
        else:
            self._data = [{'msg': f'mock data for: {query[:50]}'}]
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
