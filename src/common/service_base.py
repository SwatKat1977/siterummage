'''
Copyright (C) 2020 Trackside Manager Project

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''
import asyncio

class ServiceBase:
    """ Service base class."""

    @property
    def shutdown_completed(self) -> bool:
        """!@brief shutdown_completed property (getter).
        @param self The object pointer.
        @return True if shutdown has completed, else False.
        """
        return self._shutdown_completed

    def __init__(self):
        """!@brief Default constructor.
        @param self The object pointer.
        """

        self._is_initialised = False
        self._shutdown_completed = False
        self._shutdown_requested = False

    async def start(self) -> None:
        """!@brief ** Overridable 'run' function **
        Start the application.
        @param self The object pointer.
        @return None
        """

        if not self._is_initialised:
            raise RuntimeError('Not initialised')

        while not self._shutdown_requested:
            await self._main_loop()
            await asyncio.sleep(0.1)

        self._shutdown_completed = True

        # Perform any shutdown required.
        self._shutdown()

    def initialise(self) -> bool:
        """!@brief Service initialisation function
        Successful initialisation should set self._initialised to True.
        @param self The object pointer.
        @return True if initialise was successful, otherwise False.
        """
        return self._initialise()

    def signal_shutdown_requested(self):
        """!@brief Signal that the service should be shutdown.  This is a
        request and only once shutdown_complete is set True is it actually
        done.
        @param self The object pointer.
        @return None
        """
        self._shutdown_requested = True

    def _initialise(self) -> bool:
        """!@brief Overridable 'initialise' function **
        Successful initialisation should set self._initialised to True.
        @param self The object pointer.
        @return True if initialise was successful, otherwise False.
        """
        raise NotImplementedError("Requires implementing")

    async def _main_loop(self) -> None:
        """!@brief Overridable 'main loop' function **
        @param self The object pointer.
        @return None
        """
        raise NotImplementedError("Requires implementing")

    def _shutdown(self) -> None:
        """!@brief Overridable 'shutdown' function **
        @param self The object pointer.
        @return None
        """
