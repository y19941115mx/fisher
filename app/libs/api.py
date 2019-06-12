from flask import current_app

from app.ext import cache
from app.libs.http import HTTP


class YuShuBook:
    """
        封装鱼书API 提供数据
    """
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []
        self.per_page = current_app.config['PER_PAGE']

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = YuShuBook.get_by_api(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page):
        page = page
        url = self.keyword_url.format(keyword, self.per_page, self.per_page * (page - 1))
        result = YuShuBook.get_by_api(url)
        self.__fill_collection(result)

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    @staticmethod
    @cache.memoize(timeout=600)
    def get_by_api(url):
        return HTTP.get(url)