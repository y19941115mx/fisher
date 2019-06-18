from flask import Blueprint
from app.web import book, draft, wish, auth


def create_blueprint_web():
    blueprint = Blueprint('web', __name__, template_folder='templates')
    book.redprint.register(blueprint)
    wish.redprint.register(blueprint)
    draft.redprint.register(blueprint)
    auth.redprint.register(blueprint)
    return blueprint


bp = create_blueprint_web()


@bp.route('/')
def main():
    return 'index'
