"""应用配置管理 — 从环境变量读取，替代硬编码"""

from dataclasses import dataclass, field
from os import environ
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DBConfig:
    """数据库连接配置"""
    host: str = field(default_factory=lambda: environ.get('DB_HOST', ''))
    port: int = field(default_factory=lambda: int(environ.get('DB_PORT', '3306')))
    user: str = field(default_factory=lambda: environ.get('DB_USER', ''))
    password: str = field(default_factory=lambda: environ.get('DB_PASSWORD', ''))
    database: str = field(default_factory=lambda: environ.get('DB_NAME', ''))
    charset: str = 'utf8mb4'
    connect_timeout: int = 10


@dataclass
class AppConfig:
    """全局应用配置"""
    # 主业务库
    db: DBConfig = field(default_factory=lambda: DBConfig(
        host=environ.get('DB_HOST', ''),
        port=int(environ.get('DB_PORT', '3306')),
        user=environ.get('DB_USER', ''),
        password=environ.get('DB_PASSWORD', ''),
        database=environ.get('DB_NAME', '')
    ))
    # 备用库
    db2: DBConfig = field(default_factory=lambda: DBConfig(
        host=environ.get('DB2_HOST', ''),
        port=int(environ.get('DB2_PORT', '33973')),
        user=environ.get('DB2_USER', ''),
        password=environ.get('DB2_PASSWORD', ''),
        database=environ.get('DB2_NAME', '')
    ))

    secret_key: str = field(default_factory=lambda: environ.get('SECRET_KEY', 'dev-key-change-me'))
    debug: bool = field(default_factory=lambda: environ.get('FLASK_DEBUG', '0') == '1')

    # 外部系统
    ruoyi_base_url: str = field(default_factory=lambda: environ.get('RUOYI_BASE_URL', ''))
    static_base_url: str = field(default_factory=lambda: environ.get('STATIC_BASE_URL', ''))


config = AppConfig()
