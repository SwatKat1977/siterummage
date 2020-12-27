import hashlib
import requests
from lxml import html, etree
from http_status_code import HTTPStatusCode
from scraped_page_builder import ScrapedPageBuilder


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

    return builder.set_description(description).set_domain(domain)\
        .set_hash(hash).set_title(title).set_url_path(url_path).build()

    # print(page_contents)

def main():
    #ScrapePage('https://en.wikipedia.org/wiki/Chitty_Chitty_Bang_Bang')
    ScrapePage('https://www.tesco.com/')

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
