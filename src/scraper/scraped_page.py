
class ScrapedPage:
    __slots__ = ['_description', '_domain', '_page_hash', '_title', '_url_path']

    @property
    def description(self):
        return self._description

    @property
    def domain(self):
        return self._domain

    @property
    def page_hash(self):
        return self._page_hash

    @property
    def title(self):
        return self._title

    @property
    def url_path(self):
        return self._url_path

    def __init__(self, description, domain, page_hash, title, url_path):
        self._description = description
        self._domain = domain
        self._page_hash = page_hash
        self._title = title
        self._url_path = url_path
