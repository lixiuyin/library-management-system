"""
应用配置：优先从环境变量读取，.env 由 python-dotenv 在 work/ 目录下加载。
生产环境请务必设置所有敏感变量，勿依赖默认值。
"""
import os
from datetime import timedelta
from urllib.parse import quote_plus

# 固定从 work/ 目录加载 .env，与当前工作目录无关
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ENV_FILE = os.path.join(_BASE_DIR, '.env')

try:
    from dotenv import load_dotenv
    load_dotenv(_ENV_FILE)
except ImportError:
    pass


def _env(key: str, default: str = '') -> str:
    return (os.environ.get(key) or default).strip()


# 数据库（连 Docker MySQL 时建议用 127.0.0.1:3306，与 docker.sh 中 root@'127.0.0.1' 对应）
DB_USERNAME = _env('DB_USERNAME', 'test1')
DB_PASSWORD = _env('DB_PASSWORD', '')
_raw_host = _env('DB_HOST', 'localhost:3306')
DB_HOST = '127.0.0.1:3306' if _raw_host.strip() == 'localhost:3306' else _raw_host
DB_NAME = _env('DB_NAME', 'book_system')

# JWT
_DEV_JWT = 'dev-secret-change-in-production'
JWT_SECRET_KEY = _env('JWT_SECRET_KEY', _DEV_JWT)
JWT_EXPIRATION_DAYS = int(_env('JWT_EXPIRATION_DAYS', '1') or '1')
if _env('FLASK_ENV', 'development').lower() == 'production' and JWT_SECRET_KEY == _DEV_JWT:
    import warnings
    warnings.warn('生产环境下请设置 JWT_SECRET_KEY，勿使用默认值。', UserWarning)

# Flask 运行
FLASK_ENV = _env('FLASK_ENV', 'development')
FLASK_DEBUG = _env('FLASK_DEBUG', '1').lower() in ('1', 'true', 'yes')
FLASK_HOST = _env('FLASK_HOST', '127.0.0.1')
FLASK_PORT = int(_env('FLASK_PORT', '8080') or '8080')

# CORS：为空或 * 表示允许所有来源（开发）；生产可填前端地址，多个用逗号分隔
CORS_ORIGINS_RAW = _env('CORS_ORIGINS', '*')
CORS_ORIGINS = [o.strip() for o in CORS_ORIGINS_RAW.split(',') if o.strip()] if CORS_ORIGINS_RAW != '*' else '*'


_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
    DB_USERNAME,
    quote_plus(DB_PASSWORD),
    DB_HOST,
    DB_NAME,
)
_URI_SAFE = 'mysql+pymysql://{}:***@{}/{}'.format(DB_USERNAME, DB_HOST, DB_NAME)
print(f'[config] SQLALCHEMY_DATABASE_URI = {_URI_SAFE}')


class Config:
    """Flask 配置对象"""
    ENV = FLASK_ENV
    DEBUG = FLASK_DEBUG
    JWT_SECRET_KEY = JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=JWT_EXPIRATION_DAYS)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = _URI
