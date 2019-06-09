class Redprint(object):

    def __init__(self, name):
        self.name = name
        self.bp = None
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f
        return decorator

    def register(self, bp, url_prefix=None):
        url_prefix = url_prefix or f'/{self.name}'
        for f, rule, options in self.mound:
            endpoint = self.name + ':' + \
                       options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
