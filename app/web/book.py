import json

from flask import jsonify, render_template, flash, request

from app.forms.book import SearchForm
from app.libs.redprint import Redprint
from app.libs.util import is_isbn_or_key
from app.view_models.book import BookCollection
from app.libs.api import YuShuBook

redprint = Redprint('book')


@redprint.route('/search')
def search():
    form = SearchForm(request.args)
    books = BookCollection()
    yushu = YuShuBook()

    if form.validate():
        page = form.page.data
        q = form.q.data

        isbn_or_key = is_isbn_or_key(q)

        if isbn_or_key == 'isbn':
            yushu.search_by_isbn(q)
        else:
            yushu.search_by_keyword(q, page)

        books.fill(yushu, q)
    else:
        flash("搜索的关键字不符合要求，请重新输入关键字")

    return render_template('search_result.html', books=books)
