from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo, Regexp, length

from app.forms.base import BaseForm
from app.libs.enum import ClientTypeEnum
from app.models.user import User


class EmailForm(BaseForm):
    email = StringField('电子邮件', validators=[DataRequired(),
                                            Email(message='电子邮箱不符合规范')])


class LoginForm(EmailForm):
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 24)])


class RegisterForm(EmailForm):
    nickname = StringField('昵称', validators=[
        DataRequired(), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])

    password = PasswordField('密码', validators=[
        DataRequired(), Length(6, 20)])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')
        

class ResetPasswordForm(BaseForm):
    password1 = PasswordField('新密码', validators=[
        DataRequired(), Length(6, 20, message='密码长度至少需要在6到20个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField('确认新密码', validators=[
        DataRequired(), Length(6, 20)])


class ClientForm(BaseForm):
    account = StringField(validators=[DataRequired(message='不允许为空')])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        # self.type.data = client

    def validate_account(self, value):
        length = len(str(value)) 
        if length < 5 or length > 32:
            raise ValidationError('account的长度为5-32个字符')


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()