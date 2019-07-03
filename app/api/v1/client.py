from app.libs.redprint import Redprint

api = Redprint('client')


# @api.route('/register', methods=['POST'])
# def create_client():
#     form = ClientForm().validate_for_api()
#     promise = {
#         ClientTypeEnum.USER_EMAIL: __register_user_by_email
#     }
#     promise[form.type.data]()
#     return Success()
#
#
# def __register_user_by_email():
#     form = UserEmailForm().validate_for_api()
#     User.register_by_email(form.nickname.data,
#                            form.account.data,
#                            form.secret.data)