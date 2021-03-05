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

class ScrapeNodeEntry:
    """ Class that encapsulates details for a scrape node """
    #pylint: disable=too-few-public-methods
    __slots__ = ['_identifier']

    @property
    def identifier(self) -> str:
        """!@brief Node unique identifier (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._identifier

    def __init__(self, identifier):
        self._identifier = identifier
