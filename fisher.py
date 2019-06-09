from app import create_app
from app.models import db

app = create_app() # 默认载入开发环境配置文件


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=80)