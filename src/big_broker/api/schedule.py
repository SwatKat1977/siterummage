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

class ApiSchedule:

    def __init__(self, interface_instance, configuration):
        self._interface = interface_instance
        self._configuration = configuration

    #     # Add route : /webpage/add
    #     self._interface.add_url_rule('/webpage/add',
    #         methods = ['POST'], view_func = self._add_webpage)

    # async def _add_webpage(self) -> None:
    #     """!@brief Implementation of the /webpage/add endpoint.
    #     @param self The object pointer.
    #     @returns None.
    #     """


    ### info on job etc
    