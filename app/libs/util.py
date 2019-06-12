import random
import string


def is_isbn_or_key(word):
    word = word.strip()
    isbn_or_key = 'key'
    if check_isbn(isbn_or_key):
        isbn_or_key = 'isbn'
    return isbn_or_key


def check_isbn(isbn):
    isbn = isbn.strip()
    if len(isbn) == 13 and isbn.isdigit():
        return True
    short_word = isbn.replace('-', '')
    if len(short_word) == 10 and short_word.isdigit():
        return True
    return False



def generate_secret_key(n=50):
    seed = string.ascii_letters + '1234567890'
    sa = []
    for i in range(n):
        sa.append(random.choice(seed))

    salt = ''.join(sa)
    return salt

