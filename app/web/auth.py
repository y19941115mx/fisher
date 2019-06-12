from app.libs.redprint import Redprint

redprint = Redprint('auth')

# todo 完成登录、注册功能
@redprint.route('/login', methods=['GET', 'POST'])
def login():
    pass


@redprint.route('/register', methods=['GET', 'POST'])
def register():
    pass