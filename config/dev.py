DEBUG = True
PER_PAGE = 15
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/test'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'NGyISxDqk33xEwNP0Qi5zRT9a0t2yuTXkXzNbuzMKmemEmrBK9'
EXPIRATION_TIME = 10 * 24 * 3600

# Email 配置
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = 'victor19941115@163.com'
MAIL_PASSWORD = 'yy6689990'
MAIL_SUBJECT_PREFIX = '[鱼书]'
MAIL_DEFAULT_SENDER = '鱼书 <victor19941115@163.com>'
