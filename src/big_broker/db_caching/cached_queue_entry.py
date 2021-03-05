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
from enum import Enum

class LinkType(Enum):
    NewLink = 0
    Rescan = 1

class CachedQueueEntry:
    __slots__ = ['_id', '_insertion_date', '_link_type', '_url']

    @property
    def id(self) -> int:
        return self._id

    @property
    def url(self) -> str:
        return self._url

    @property
    def insertion_date(self) -> int:
        return self._insertion_date

    @property
    def link_type(self) -> LinkType:
        return self._link_type

    def __init__(self, id, url, insert_date, link_type):
        self._id = id
        self._url = url
        self._insertion_date = insert_date
        self._link_type = link_type
