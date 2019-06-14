from flask import Blueprint
from app.web import book, draft, wish, auth


def create_blueprint_web():
    blueprint = Blueprint('web', __name__, template_folder='templates')
    book.redprint.register(blueprint) # 为蓝图注册模块
    wish.redprint.register(blueprint) # 为蓝图注册模块
    draft.redprint.register(blueprint) # 为蓝图注册模块
    auth.redprint.register(blueprint) # 为蓝图注册模块
    return blueprint


bp = create_blueprint_web()


@bp.route('/')
def main():
    return 'index'
