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

class Event:
    ''' Implementation of an event. '''
    __slots__ = ['_event_id', '_msg_body', '_trigger_time']

    @property
    def event_id(self) -> object:
        """!@brief Event ID (Getter).
        @param self The object pointer.
        @returns An object.
        """
        return self._event_id

    @property
    def body(self) -> object:
        """!@brief Event body (Getter).
        @param self The object pointer.
        @returns An object.
        """
        return self._msg_body

    @property
    def trigger_time(self) -> int:
        """!@brief Optional trigger time, 0 if no trigger time (Getter).
        @param self The object pointer.
        @returns int.
        """
        return self._trigger_time

    @trigger_time.setter
    def trigger_time(self, new_time) -> None:
        """!@brief Optional trigger time, 0 if no trigger time (Setter).
        @param self The object pointer.
        @returns None.
        """
        self._trigger_time = new_time

    def __init__(self, event_id, msg_body=None, trigger_time=0):
        """!@brief Event class constructor.
        @param self The object pointer.
        @param event_id Id of event.
        @param msg_body Optional message body for event (milliseconds).
        @return Event instance.
        """
        self._event_id = event_id
        self._msg_body = msg_body
        self._trigger_time = trigger_time
