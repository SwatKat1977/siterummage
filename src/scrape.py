import hashlib
import requests
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
from lxml import html, etree
from http_status_code import HTTPStatusCode

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
    def url_path(self):
        return self._url_path

    def __init__(self, description, domain, page_hash, url_path):
        self._description = description
        self._domain = domain
        self._page_hash = page_hash
        self._url_path = url_path


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
                           self._url_path)

    def reset(self):
        self._description = ''
        self._domain = None
        self._hash = None
        self._title = ''
        self._url_path = None

Website_http = 'http://'
Website_https = 'https://'

Website_types = {
    'http' : 7,
    'https' : 8
}

def ScrapePage(url):
    builder = ScrapedPageBuilder()

    description = ''
    domain = None
    hash = None
    title = ''
    url_path = ''

    user_agent = {'User-agent': 'Mozilla/5.0'}
    page = requests.get(url, headers = user_agent)

    if page.status_code != HTTPStatusCode.OK:
        print(f"URL '{url} returned status code {page.status_code}")
        return

    index_for_domain = -1
    if url.startswith(Website_http):
        index_for_domain = Website_types['http']

    elif url.startswith(Website_https):
        index_for_domain = Website_types['https']

    domain_index = url.rfind('/', index_for_domain)

    if domain_index != -1:
        domain = url[0:domain_index]
        url_path = url[domain_index:]

    else:
        domain = url
        url_path = '/'

    html_tree = html.fromstring(page.content)
    page_contents = etree.tostring(html_tree)

    hash = hashlib.md5(page_contents).hexdigest()

    # Get meta data for page from head.
    for child in html_tree.head:
        if child.tag == 'title':
            title = child.text

        elif child.tag == 'meta':
            if 'name' in child.attrib and  child.attrib['name'] == 'description':
                if 'content' in child.attrib:
                    description = child.attrib['content']

    print(f'Title:       {title}')
    print(f"Description: {description}")
    print(f'MD5 Hash:    {hash}')
    print(f'Domain:      {domain}')
    print(f'url path:    {url_path}')

    return ScrapedPage(description, domain, hash, url_path)

    #print(dir(html_tree))

    # print(page_contents)

def main():
    #ScrapePage('https://en.wikipedia.org/wiki/Chitty_Chitty_Bang_Bang')
    ScrapePage('https://www.tesco.com')

    # return

    # print(etree.tostring(html_tree))

    # print(html_tree)
    # print(dir(html_tree))

    # print('<== Head ==>')
    # for child in html_tree.head:
    #     print(child)

    # print(etree.tostring(html_tree.body))

    # print('<== Body ==>')
    # for child in html_tree.body:
    #     print(child)

    # print(html_tree.body.tag)

main()
