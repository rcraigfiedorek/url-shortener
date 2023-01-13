from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(
    engine_options=dict(pool_size=5, max_overflow=2, pool_timeout=30, pool_recycle=1800)
)
