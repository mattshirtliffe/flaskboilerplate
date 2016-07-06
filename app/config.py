class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SECRET_KEY='secret key'

class LinuxProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'

class WindowsProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'

class LinuxDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

class WindowsDevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    USERNAME ='testuser'
    PASSWORD = 'password'
    TESTING = True