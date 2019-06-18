def hello(s=1, dic = None):
    if dic is None:
        dic = {}
    print(s, dic)


if __name__ == '__main__':
    res = dict(s=1, b=2)
    hello(1, res)
    print(res)