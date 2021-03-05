'''
Copyright 2021 Siterummage

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import hashlib
from typing import Tuple
import requests
from lxml import html, etree
from common.event import Event
from common.http_status_code import HTTPStatusCode
from common.logger import LogType
from common.url_utils import UrlUtils
from event_id import EventID
from scraped_page_builder import ScrapedPageBuilder

class PageScraper:
    ''' Class that emcompasses getting a page and scraping it '''
    #pylint: disable=too-few-public-methods
    __slots__ = ['_event_manager', '_logger', '_page_builder',
                 '_scrape_successful', '_task_type', '_task_id',
                 '_url_being_processed', '_user_agent']

    @property
    def url_being_processed(self) -> str:
        """!@brief Url being processed (Getter).
        @param self The object pointer.
        @returns boolean if connected or not.
        """
        return self._url_being_processed

    @property
    def was_scrape_successful(self) -> bool:
        """!@brief Was scrape successful flag (Getter).
        @param self The object pointer.
        @returns boolean to indicate if scrape was successful.
        """
        return self._scrape_successful

    def __init__(self, logger, event_manager):
        self._event_manager = event_manager
        self._logger = logger
        self._page_builder = ScrapedPageBuilder()
        self._user_agent = {'User-agent': 'Mozilla/5.0'}
        self._url_being_processed = None
        self._scrape_successful = False
        self._task_type = None
        self._task_id = None

    def scrape_page(self, url, task_type, task_id) -> Tuple[list, dict]:
        """!@brief Take a url and attempt to scrape meta data and links from it.
        @param self The object pointer.
        @param url URL to read.
        @returns None.
        """
        #pylint: disable=too-many-locals

        self._url_being_processed = url
        self._task_type = task_type
        self._task_id = task_id
        self._scrape_successful = False

        description = ''
        title = ''

        url_details = UrlUtils.split_url_into_domain_and_page(url)

        self._page_builder.reset()

        page = self._read_page(url)
        if not page:
            self._url_being_processed = None

            self._logger.log(LogType.Info, f"URL '{url}' is unreachable")
            page_details = self._page_builder.set_hash('0X0DEAD').\
                set_domain(url_details['domain']).\
                set_url_path(url_details['url_path']).build()
            return [], self._generate_results(page_details, False, task_id)

        html_tree = html.fromstring(page.content)
        page_contents = etree.tostring(html_tree)

        page_hash = hashlib.md5(page_contents).hexdigest()

        # Get meta data for page from head.
        for child in html_tree.head:
            if child.tag == 'title':
                title = child.text

            elif child.tag == 'meta':
                if 'name' in child.attrib and  child.attrib['name'] == 'description':
                    if 'content' in child.attrib:
                        description = child.attrib['content']

        self._logger.log(LogType.Info, '----- Scraped Page Information -----')
        self._logger.log(LogType.Info, f'Title:       {title}')
        self._logger.log(LogType.Info, f'Description: {description}')
        self._logger.log(LogType.Info, f"MD5 Hash:    {page_hash}")
        self._logger.log(LogType.Info, f"Domain:      {url_details['domain']}")
        self._logger.log(LogType.Info, f"url path:    {url_details['url_path']}")

        links = self._extract_links_from_page(html_tree)
        self._logger.log(LogType.Info, f'Total links: {len(links)}')
        self._logger.log(LogType.Info, '------------------------------------')

        self._url_being_processed = None

        page_details = self._page_builder.set_description(description). \
            set_domain(url_details['domain']).set_hash(page_hash). \
            set_title(title).set_url_path(url_details['url_path']).build()
        return links, self._generate_results(page_details, True, task_id)

    def _read_page(self, url) -> requests.models.Response:
        """!@brief Attempt to read a webpage by making a get on the page, on a
                   successful read a response is returned, otherwise None is.
        @param self The object pointer.
        @param url URL to read.
        @returns Response is returned on successful, otherwise None is.
        """

        try:
            page = requests.get(url, headers = self._user_agent,
            timeout=(2, 2))

        except requests.exceptions.ConnectionError:
            return None

        if page.status_code != HTTPStatusCode.OK:
            print(f"URL '{url} returned status code {page.status_code}")
            return None

        return page

    def _extract_links_from_page(self, html_tree):
        #pylint: disable=no-self-use

        # Extract all of the hrefs from the webpage.
        all_links = list(html_tree.xpath('//a/@href'))

        # Remove duplicates.
        all_links = list(dict.fromkeys(all_links))

        # Remove interal links and other invalid paths.
        all_links = [link for link in all_links if len(link)]
        all_links = [link for link in all_links if link[0] != '#' and link[0] != '/']
        return all_links

    ##def results = self._generate_results(page_details, False, task_id)
    def _generate_results(self, details, success, task_id):
        #pylint: disable=too-many-arguments

        send_event_body = {
            'details': details.build_json(),
            'success': success,
            'task_id': task_id
        }

        return send_event_body
