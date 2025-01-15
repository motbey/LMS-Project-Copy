SQLALCHEMY_DATABASE_URI = 'sqlite:///lms.db'
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'connect_args': {
        'timeout': 30,
        'check_same_thread': False
    },
    'pool_size': 10,
    'max_overflow': 5
}
SQLALCHEMY_TRACK_MODIFICATIONS = False 