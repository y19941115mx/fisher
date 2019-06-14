from app.libs.redprint import Redprint
from flask import render_template, request
from app.forms.auth import LoginForm, RegisterForm

redprint = Redprint('auth')


@redprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     # 登陆逻辑
    #     pass
    return render_template('/auth/login.html', form=form)


@redprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    return render_template('/auth/register.html',form=form)