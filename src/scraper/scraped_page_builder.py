from scraped_page import ScrapedPage

class ScrapedPageBuilder:
    __slots__ = ['_description', '_domain', '_hash', '_title', '_url_path']

    def set_description(self, value):
        self._description = value
        return self

    def set_domain(self, value):
        self._domain = value
        return self

    def set_hash(self, value):
        self._hash = value
        return self

    def set_title(self, value):
        self._title = value
        return self

    def set_url_path(self, value):
        self._url_path = value
        return self

    def __init__(self):
        self._description = ''
        self._domain = None
        self._hash = None
        self._title = ''
        self._url_path = None

    def build(self):
        if not self._domain:
            raise AttributeError('Missing domain attribute')

        if not self._hash:
            raise AttributeError('Missing hash attribute')

        if not self._url_path:
            raise AttributeError('Missing url path attribute')

        return ScrapedPage(self._description, self._domain,  self._hash,
                           self._title, self._url_path)

    def reset(self):
        self._description = ''
        self._domain = None
        self._hash = None
        self._title = ''
        self._url_path = None
