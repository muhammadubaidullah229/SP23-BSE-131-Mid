import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sp23-bse-131-mid-exam-secret-key-default')
    
    # Database Configuration:
    # First check DATABASE_URL, then build from individual DB_* environment variables,
    # and gracefully fallback to SQLite if PostgreSQL is not specified (e.g. during local tests)
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST', 'db')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME')

    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    elif DB_USER and DB_PASSWORD and DB_NAME:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        # Fallback for local quick testing outside Docker
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, 'sp23_bse_131.db').replace('\\', '/')
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
