"""数据库连接管理 — 使用上下文管理器，支持连接池"""

from contextlib import contextmanager
import pymysql
from pymysql.cursors import DictCursor
from backend.config import config


class DatabaseManager:
    """数据库连接管理器

    使用 contextmanager 确保每个请求正确获取/释放连接。
    后续可扩展为真正的连接池（如 SQLAlchemy 或 DBUtils）。
    """

    def __init__(self, db_config: 'DBConfig'):
        self.config = db_config
        self._conn = None

    @contextmanager
    def get_conn(self):
        """获取数据库连接（上下文管理器，自动提交/回滚/关闭）"""
        conn = pymysql.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.user,
            password=self.config.password,
            database=self.config.database,
            charset=self.config.charset,
            connect_timeout=self.config.connect_timeout,
            cursorclass=DictCursor
        )
        try:
            yield conn
            conn.commit()
        except pymysql.MySQLError as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def test_connection(self) -> bool:
        """测试数据库连接是否正常"""
        try:
            with self.get_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1 AS ok")
                    return cursor.fetchone()['ok'] == 1
        except Exception:
            return False


# 实例化两个数据库连接管理器
db = DatabaseManager(config.db)
db2 = DatabaseManager(config.db2)
