from flask_login import login_user

from app.libs.redprint import Redprint
from flask import render_template, request, flash, redirect, url_for
from app.forms.auth import LoginForm, RegisterForm
from app.libs.util import send_email
from app.models.user import User


redprint = Redprint('auth')


@redprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.is_active and user.check_password(form.password.data):
                login_user(user, remember=True)
                # 处理重定向
                next = request.args.get('next')
                if next and str(next).startswith('/'):
                    return redirect(next)
                else:
                    return redirect(url_for('web.main'))
            else:
                flash('账号未激活或密码错误')
        else:
            flash('账户不存在')

    return render_template('auth/login.html', form=form)


@redprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User().set_attrs(form.data)
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
    pass