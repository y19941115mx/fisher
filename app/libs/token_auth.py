from collections import namedtuple

from flask import current_app, request, g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.libs.exception import AuthFailed, Forbidden
from app.libs.scope import is_in_scope


def generate_token(data=None, expiration=600):
    if data is None:
        data = {}
    expiration = current_app.config.get('EXPIRATION_TIME') or expiration
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps(data).decode('ascii')


def translate_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token.encode('ascii'))
    except:
        return None
    return data


# token auth验证

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'ac_type', 'scope'])


@auth.verify_password
def verify_password(token, password):
    # token
    # HTTP 账号密码
    # header key:value
    # account  qiyue
    # 123456
    # key=Authorization
    # value =basic base64(qiyue:123456)
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        # request
        g.user = user_info
        return True


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid',
                         error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired',
                         error_code=1003)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    # 权限控制
    # allow = is_in_scope(scope, request.endpoint)
    # if not allow:
    #     raise Forbidden()
    return User(uid, ac_type, scope)
