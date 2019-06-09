import json

from flask import request, jsonify

from app.forms.book import SearchForm
from app.libs.redprint import Redprint
from app.libs.util import is_isbn_or_key
from app.view_models.book import BookCollection
from app.libs.http import YuShuBook
from app.models import book

redprint = Redprint('book')


@redprint.route('/search')
def search():
    form = SearchForm(request.args)
    if form.validate():
        books = BookCollection()
        yushu = YuShuBook()
        page = form.page.data
        q = form.q.data
        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == 'isbn':
            yushu.search_by_isbn(q)
        else:
            yushu.search_by_keyword(q, page)

        books.fill(yushu, q)
        json_str = json.dumps(books, default=lambda x:x.__dict__, ensure_ascii=False)

        return json_str, {'content-type': 'application/json'}

    return jsonify({'msg': 'wrong msg'})
