'''
Copyright (C) 2021 Siterummage
All Rights Reserved.

NOTICE:  All information contained herein is, and remains the property of
Siterummage.  The intellectual and technical concepts contained herein are
proprietary to Siterummage and may be covered by U.K. and Foreign Patents,
patents in process, and are protected by trade secret or copyright law.
Dissemination of this information or reproduction of this material is strictly
forbidden unless prior written permission is obtained from Siterummage.
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
