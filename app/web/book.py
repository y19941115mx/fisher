import json

from flask import jsonify, render_template, flash, request

from app.forms.book import SearchForm
from app.libs.redprint import Redprint
from app.libs.util import is_isbn_or_key, check_isbn
from app.view_models.book import BookViewCollection, BookViewModel
from app.libs.api import YuShuBook

redprint = Redprint('book')


@redprint.route('/search')
def search():
    form = SearchForm(request.args)
    books = BookViewCollection()
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


@redprint.route('/<isbn>/detail')
def detail(isbn):
    has_in_gifts = False
    has_in_wishes = False
 
    yushu = YuShuBook()

    if check_isbn(isbn):
        yushu.search_by_isbn(isbn)
        book = BookViewModel(yushu.first)
    else:
        flash('isbn号不符合要求，请重新输入')

    return render_template('book_detail.html', book=book,
                           wishes=None, gifts=None,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)
