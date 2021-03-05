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
#pylint: disable=wrong-import-position
import os
import sys
sys.path.insert(0, '.')
from scrape_node_app import ScrapeNodeApp

app = ScrapeNodeApp()

if not os.getenv('SITERUMMAGE_SCRAPENODE_CONFIG'):
    print('[ERROR] SITERUMMAGE_SCRAPENODE_CONFIG environment variable is' + \
                      ' not defined!')
    sys.exit(1)

if not os.getenv('SITERUMMAGE_SCRAPENODE_MESSAGING_CONFIG'):
    print('[ERROR] SITERUMMAGE_SCRAPENODE_MESSAGING_CONFIG environment' + \
                      ' variable is not defined!')
    sys.exit(1)

if not app.initialise():
    sys.exit()

app.start()
