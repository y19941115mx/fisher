from flask import request, current_app

from app.forms.auth import ClientForm, UserPhoneForm
from app.libs.enum import ClientTypeEnum
from app.libs.exception import AuthFailed, ParameterException, Success
from app.libs.redprint import Redprint
from leancloud import cloud

from app.libs.token_auth import generate_token
from app.libs.util import jsonify
from app.models import db
from app.models.user import User

api = Redprint('auth')

# with current_app.app_context():
    # leancloud.init(current_app.config['LEAN_APP_ID'], current_app.config['LEAN_APP_KEY'])

@api.route('/sms', methods=['POST'])
def send_sms():
    json = request.get_json()
    phone_num = json.get('phone_num', '')
    if not phone_num:
        raise ParameterException()

    cloud.request_sms_code(phone_num)
    raise Success


@api.route('/login', methods=['POST'])
def login():
    form = ClientForm().validate_for_api()

    promise = {
        ClientTypeEnum.USER_MOBILE: verify_moble,
    }

    identity = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )
    # Token
    data = dict(uid=identity['uid'], type=form.type.data, scope=identity['scope'])
    token = generate_token(data)

    return jsonify(token=token)


def verify_moble(phone, code):
    form = UserPhoneForm().validate_for_api()
    is_login = cloud.verify_sms_code(form.account.data, form.secret.data)
    if not is_login:
        raise AuthFailed()
    user = User.query.filter_by(phone_number=str(phone)).first()
    if not user:
        with db.auto_commit():
            user = User()
            user.phone_number = phone
            user.add()
    return dict(uid=user.id, scope=user.scope)
