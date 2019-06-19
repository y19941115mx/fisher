from flask_login import login_user, logout_user

from app.libs.redprint import Redprint
from flask import render_template, request, flash, redirect, url_for
from app.forms.auth import LoginForm, RegisterForm, EmailForm, ResetPasswordForm
from app.libs.token import translate_token
from app.libs.util import send_email
from app.models import db
from app.models.user import User

redprint = Redprint('auth')


@redprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user.is_active and user.check_password(form.password.data):
            login_user(user, remember=True)
            # 处理重定向
            next = request.args.get('next')
            if next and str(next).startswith('/'):
                return redirect(next)
            else:
                return redirect(url_for('web.index'))
        else:
            flash('账号未激活或密码错误')

    return render_template('auth/login.html', form=form)


@redprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User().set_attrs(form.data)
        with db.auto_commit():
            user.add()
        send_email(user.email, '激活你的账户', 'email/confirm.html', token=user.generate_token())
        flash('Email has been sent!Please confirm the login message')
        return redirect(url_for('web.auth:login'))

    return render_template('auth/register.html', form=form)


@redprint.route('/confirm/<token>')
def confirm(token):
    if User.confirm_token(token):
        flash('activate success, please login in !')
    else:
        flash('activate fail, token may has been expired !')
    return redirect(url_for('web.auth:login'))


@redprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))


@redprint.route('/forget/password', methods=['GET', 'POST'])
def forget_password():
    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():

        user = User.query.filter_by(email=form.email.data).first_or_404()
        send_email(user.email, '重置你的密码', 'email/reset_password.html',
                   user=user, token=user.generate_token())

        flash('发送邮件成功，请注意查收')

    return render_template('auth/forget_password_request.html', form=form)


@redprint.route('/reset/password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    data = translate_token(token)

    if data:
        uid = int(data['id'])
        user = User.query.filter_by(id=uid).first_or_404()
    else:
        flash('token已失效，请重新获取')
        return redirect(url_for('web.auth:forget_password'))

    form = ResetPasswordForm(request.form)

    if request.method == 'POST' and form.validate():

        with db.auto_commit():
            user.password = form.password1.data

        flash('修改密码成功，请重新登录')
        return redirect(url_for('web.auth:login'))

    return render_template('auth/forget_password.html', form=form)

