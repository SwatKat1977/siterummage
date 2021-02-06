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
from .scrape_node_entry import ScrapeNodeEntry

class ScrapeNodeList:
    """ List of connected Scrape Nodes """
    __slots__ = ['_nodes']

    def __init__(self) -> object:
        """!@brief ScrapeNodeList constructor.
        @param self The object pointer.
        @returns object.
        """
        self._nodes = {}

    def add_node(self, node) -> bool:
        """!@brief Add a scrape node to the list. If the node exists then
                   False is returned, otherwise True.
        @param self The object pointer.
        @param node Node to be added.
        @returns True = Succcess, False = Failure (already exists).
        """

        if node.identifier in self._nodes:
            return False

        self._nodes[node.identifier] = node
        return True

    def del_node(self, node_identifier) -> None:
        """!@brief Delete a scrape node from the list. If the node doesn't
                   exists then an exception of RuntimeError is raised.
        @param self The object pointer.
        @param node_identifier Identifier of node to be deleted.
        @returns object.
        """

        try:
            return self._nodes[node_identifier]

        except KeyError:
            return None

    def get_node(self, node_identifier) -> ScrapeNodeEntry:
        """!@brief Get a scrape node on the list. If the node doesn't
                   exists then None is returned.
        @param self The object pointer.
        @param node_identifier Identifier of node to retrieve.
        @returns object.
        """

        try:
            return self._nodes[node_identifier]

        except KeyError:
            return None

    def get_all_node(self) -> dict:
        """!@brief Get all scrape nodes in the list.
        @param self The object pointer.
        @returns dict containing all nodes.
        """

        return self._nodes

    def node_exists(self, node_identifier) -> bool:
        """!@brief Check to see if a scrape node exists in the list.
        @param self The object pointer.
        @param node_identifier Identifier of node to check.
        @returns True = exists, False = doesn't exist.
        """
        return node_identifier in self._nodes
