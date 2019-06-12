from app.libs.redprint import Redprint

redprint = Redprint('wish')


@redprint.route('/book/<isbn>')
def save_to_wish():
    pass


@redprint.route('/satisfy/<int:wid>')
def satisfy_wish(wid):
    pass
