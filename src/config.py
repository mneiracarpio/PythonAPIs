class DevelopmentConfig():
    DEBUG = True
    DB_USERNAME = 'scott'
    DB_PASSWORD = 'tiger'
    DB_DSN = 'localhost:1521/XEPDB1'
    DB_ENCODING = 'UTF-8'

config = {
    'development' : DevelopmentConfig
}