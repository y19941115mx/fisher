from flask import jsonify, request, current_app

from app.libs.redprint import Redprint
from app.models.tcl import Healthy, Notice, Article
from app.libs.token_auth import auth
from flask import g

api = Redprint('tcl')

@api.route('/healthy')
@auth.login_required
def get_healthy_msg():
    uid = g.user.uid
    msg = Healthy.query.filter_by(uid=uid).first_or_404_api()
    return jsonify(msg)


@api.route('/notice')
def get_notice():
    msg = Notice.query.limit(1).first_or_404_api()
    return jsonify(msg)


@api.route('/article')
def get_article():
    page = request.args.get('page', 1)
    per_page = current_app.config['PER_PAGE'] or 15
    offset = per_page * (page - 1)
    articles = Article.query.filter_by().offset(offset).all()
    return jsonify(articles)