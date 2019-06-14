from app.libs.redprint import Redprint
from flask_login import login_required

redprint = Redprint('wish')


@redprint.route('/book/<int:isbn>')
@login_required
def save_to_wish(isbn):
    return 'hello'


@redprint.route('/satisfy/<int:wid>')
def satisfy_wish(wid):
    return 'hello'
