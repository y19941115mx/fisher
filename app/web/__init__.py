from flask import Blueprint, render_template
from werkzeug.exceptions import HTTPException

from app.libs.util import jsonify
from app.models.gift import Gift
from app.models.user import User
from app.view_models.book import BookViewModel
from app.web import book, drift, wish, auth, gift


def create_blueprint_web():
    blueprint = Blueprint('web', __name__, template_folder='templates')
    book.redprint.register(blueprint)
    wish.redprint.register(blueprint)
    drift.redprint.register(blueprint)
    auth.redprint.register(blueprint)
    gift.redprint.register(blueprint)
    return blueprint


bp = create_blueprint_web()


@bp.route('/')
def index():
    gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in gifts]
    # return render_template('index.html', recent=books)








