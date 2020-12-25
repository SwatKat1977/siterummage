import hashlib
import requests
from lxml import html, etree

def main():
    print('main...')

    page = requests.get('https://en.wikipedia.org/wiki/Chitty_Chitty_Bang_Bang')

    html_tree = html.fromstring(page.content)
    page_contents = etree.tostring(html_tree)

    hash = hashlib.md5(page_contents).hexdigest()
    print(f'MD5 Hash for page: {hash}')

    # return

    # print(etree.tostring(html_tree))

    # print(html_tree)
    # print(dir(html_tree))

    print('<== Head ==>')
    for child in html_tree.head:
        print(child)

    # print(etree.tostring(html_tree.body))

    # print('<== Body ==>')
    # for child in html_tree.body:
    #     print(child)

    # print(html_tree.body.tag)

main()
