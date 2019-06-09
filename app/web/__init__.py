from flask import Blueprint
from app.web import book


def create_blueprint_web():
    blueprint = Blueprint('web', __name__, template_folder='templates')
    book.redprint.register(blueprint) # 为蓝图注册模块
    return blueprint


bp = create_blueprint_web()
