from app.libs.redprint import Redprint

redprint = Redprint('draft')


@redprint.route('/<int:gid>', methods=['GET', 'POST'])
def send_drift(gid):
    pass