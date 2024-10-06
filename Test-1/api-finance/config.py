class Config(object):
    """Base config, uses staging database server."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_API_ENABLED = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return 'mysql://{}:{}@{}:3306/{}'.format(self.DB_USER, self.DB_PASS, self.DB_HOST, self.DB_NAME)

class ProductionConfig(Config):
    DB_HOST = 'localhost'
    DB_NAME = 'db_mnc_finance'
    DB_USER = 'root'
    DB_PASS = ''

class DevelopmentConfig(Config):
    DB_HOST = 'localhost'
    DB_NAME = 'db_mnc_finance'
    DB_USER = 'root'
    DB_PASS = ''
    DEBUG = True
