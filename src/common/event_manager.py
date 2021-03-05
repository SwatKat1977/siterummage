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
import time

class EventManager:
    """ Event Manager implementation. """
    __slots__ = ['_callback_event_handlers', '_enabled', '_events',
                 '_event_handlers']

    def __init__(self):
        """!@brief Event manager class constructor.
        @param self The object pointer.
        @returns EventManager.
        """
        self._callback_event_handlers = {}
        self._enabled = True
        self._event_handlers = {}
        self._events = []
 
    def queue_event(self, event):
        """!@brief Queue a new event, it will raise an exception if the event
                   manager is disabled or the event ID has not been registered.
        @param self The object pointer.
        @param event Event to queue.
        @returns None.
        """

        # Only queue the event, if event manager is enabled (running)
        if not self._enabled:
            raise RuntimeError('Event Manager disabled')

        # Add event to queue.  Validate that the event is known about, if it is
        # then add it to the event queue for processing otherwise return
        # unknown status.
        if not self._is_valid_event(event.event_id):
            raise RuntimeError('Invalid event ID')

        if event.trigger_time:
            new_time = round(time.time() * 1000) + event.trigger_time
            event.trigger_time = new_time

        # Add the event into the queue.
        self._events.append(event)

    def callback_event(self, event):
        """!@brief Make an event callback, it will raise an exception if the
                   event manager is disabled or the event ID has not been
                   registered.
        @param self The object pointer.
        @param event Event to queue.
        @returns None.
        """

        # Only queue the event, if event manager is enabled (running)
        if not self._enabled:
            raise RuntimeError('Event Manager disabled')

        # Add event to queue.  Validate that the event is known about, if it is
        # then add it to the event queue for processing otherwise return
        # unknown status.
        if event.event_id not in self._callback_event_handlers:
            raise RuntimeError('Invalid event ID')

        #  Call the event processing function, this is defined by the
        #  registered callback function.
        return self._callback_event_handlers[event.event_id](event)

    def register_callback_event(self, event_id, callback) -> None:
        """!@brief Register a callback event with the event manager.
        @param self The object pointer.
        @param event_id ID of event to register.
        @param callback Event callback function.
        @returns None.
        """

        if event_id in self._callback_event_handlers:
            return

        self._callback_event_handlers[event_id] = callback

    def register_event(self, event_id, callback) -> None:
        """!@brief Register an event with the event manager.
        @param self The object pointer.
        @param event_id ID of event to register.
        @param callback Event callback function.
        @returns None.
        """

        if event_id in self._event_handlers:
            return

        self._event_handlers[event_id] = callback

    async def process_next_event(self) -> None:
        """!@brief Process the next event, if any exists.  An error will be
                   generated if the event ID is invalid (should never happen).
        @param self The object pointer.
        @returns True - None.
        """

        # If nothing is ready for processing just return success (True).
        if not self._events:
            return

        for idx, event in enumerate(self._events):
            now = round(time.time() * 1000)

            if event.trigger_time and now < event.trigger_time:
                continue

            #  Call the event processing function, this is defined by the
            #  registered callback function.
            self._event_handlers[event.event_id](event)

            #  Once the event has been handled, delete it.. The event handler
            # function should deal with issues with the event and therefore
            #  deleting should be safe.
            self._events.pop(idx)

            return

    def process_next_event_sync(self) -> None:
        """!@brief Process the next event, if any exists.  An error will be
                   generated if the event ID is invalid (should never happen).
        @param self The object pointer.
        @returns True - None.
        """

        # If nothing is ready for processing just return success (True).
        if not self._events:
            return

        for idx, event in enumerate(self._events):
            now = round(time.time() * 1000)

            if event.trigger_time and now < event.trigger_time:
                continue

            #  Call the event processing function, this is defined by the
            #  registered callback function.
            self._event_handlers[event.event_id](event)

            #  Once the event has been handled, delete it.. The event handler
            # function should deal with issues with the event and therefore
            #  deleting should be safe.
            self._events.pop(idx)

            return

    def delete_all_events(self) -> None:
        """!@brief Delete all events.
        @param self The object pointer.
        @return None.
        """
        del self._events[:]

    def _is_valid_event(self, event_id):
        """!@brief Check if an event is valid.
        @param self The object pointer.
        @param event_id Event ID to validate.
        @returns boolean: valid = True, invalid = False.
        """
        return event_id in self._event_handlers
