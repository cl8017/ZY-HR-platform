"""数据模型 — 数据库连接管理，使用上下文管理器，支持连接池"""

from contextlib import contextmanager
import pymysql
from pymysql.cursors import DictCursor
from backend.config import DBConfig
from backend.config import config
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """数据库连接管理器"""

    def __init__(self, db_config: DBConfig):
        self.config = db_config

    @contextmanager
    def get_conn(self):
        """获取数据库连接（上下文管理器，自动提交/回滚/关闭）"""
        if not self.config.host:
            raise ConnectionError("数据库配置为空，请检查 .env 文件")

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
            logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            conn.close()

    def test_connection(self) -> bool:
        try:
            with self.get_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1 AS ok")
                    return cursor.fetchone()['ok'] == 1
        except Exception as e:
            logger.warning(f"数据库连接测试失败: {e}")
            return False


# 实例化两个数据库连接管理器
db = DatabaseManager(config.db)
db2 = DatabaseManager(config.db2)
