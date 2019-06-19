import json

from flask import jsonify, render_template, flash, request
from flask_login import current_user

from app.forms.book import SearchForm
from app.libs.redprint import Redprint
from app.libs.util import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.book import BookViewCollection, BookViewModel
from app.libs.api import YuShuBook
from app.view_models.trade import TradeInfo

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


@redprint.route('/<isbn>')
def detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    yushu = YuShuBook()
    yushu.search_by_isbn(isbn)
    book = BookViewModel(yushu.first)

    if current_user.is_authenticated:
        has_in_gifts = current_user.is_in_gifts(isbn)
        has_in_wishes = current_user.is_in_wishes(isbn)

    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)

    return render_template('book_detail.html', book=book,
                           wishes=trade_wishes_model, gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)
