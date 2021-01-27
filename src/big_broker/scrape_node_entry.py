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
    __slots__ = ['_identifier', '_host', '_port']

    @property
    def identifier(self) -> str:
        """!@brief Node unique identifier (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._identifier

    @property
    def host(self) -> str:
        """!@brief Node hostname or IP address (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._host

    @property
    def port(self) -> int:
        """!@brief Node hostname network port (Getter).
        @param self The object pointer.
        @returns int.
        """
        return self._port

    def __init__(self, identifier, host, port):
        self._identifier = identifier
        self._host = host
        self._port = port
