"""
ZY-HR 配置管理 - 从环境变量读取，替代硬编码
"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))


@dataclass
class DBConfig:
    host: str = field(default_factory=lambda: os.getenv('DB1_HOST', 'localhost'))
    port: int = field(default_factory=lambda: int(os.getenv('DB1_PORT', '3306')))
    user: str = field(default_factory=lambda: os.getenv('DB1_USER', 'root'))
    password: str = field(default_factory=lambda: os.getenv('DB1_PASSWORD', ''))
    database: str = field(default_factory=lambda: os.getenv('DB1_DATABASE', 'test'))
    charset: str = 'utf8mb4'
    connect_timeout: int = 10


@dataclass
class AppConfig:
    db1: DBConfig = field(default_factory=DBConfig)
    db2: DBConfig = field(default_factory=lambda: DBConfig(
        host=os.getenv('DB2_HOST', 'localhost'),
        port=int(os.getenv('DB2_PORT', '33973')),
        user=os.getenv('DB2_USER', 'root'),
        password=os.getenv('DB2_PASSWORD', ''),
        database=os.getenv('DB2_DATABASE', 'yancao'),
    ))
    secret_key: str = field(default_factory=lambda: os.getenv('SECRET_KEY', 'dev-key'))
    debug: bool = field(default_factory=lambda: os.getenv('FLASK_DEBUG', '1') == '1')
    host: str = field(default_factory=lambda: os.getenv('HOST', '0.0.0.0'))
    port: int = field(default_factory=lambda: int(os.getenv('PORT', '58000')))
    mock_db: bool = field(default_factory=lambda: os.getenv('MOCK_DB', '1') == '1')


config = AppConfig()
