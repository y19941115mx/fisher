import random
import string


def is_isbn_or_key(word):
    word = word.strip()
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_word = word.replace('-', '')
    if len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key


def generate_app():
    seed = string.ascii_letters + '1234567890'
    sa = []
    for i in range(11):
        sa.append(random.choice(seed))

    salt = ''.join(sa)
    return salt

