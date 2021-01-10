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
import enum
import logging
import time

class LogType(enum.Enum):
    """ Enumeration of log type """

    ## Information that is diagnostically helpful to people more than just
    #  developers (IT, sysadmins, etc.).
    Debug = 0

    ## Generally useful information to log (service start/stop, configuration
    #  assumptions, etc). Info I want to always have available but usually
    #  don't care about under normal circumstances.
    Info = 1

    ## Anything that can potentially cause application oddities, but for which
    #  I am automatically recovering. (Such as switching from a primary to
    #  backup server, retrying an operation, missing secondary data, etc.)
    Warn = 2

    ## Any error which is fatal to the operation, but not the service or
    #  application (can't open a required file, missing data, etc.). These
    #  errors will force user (administrator, or direct user) intervention.
    Error = 3

    ## Any error that is forcing a shutdown of the service or application to
    #  prevent data loss (or further data loss). I reserve these only for the
    #  most heinous errors and situations where there is guaranteed to have
    #  been data corruption or loss.
    Critical = 4

class Logger:
    """ Logger class that can write to a console or an external logger """
    ## Static list of attributes for the Logger class.
    __slots__ = ['_external_logger', '_is_initialised', '_logger_instance',
                 '_write_to_console']

    ## Mapping of human-readable log type to the Python logging type.
    Logger_mappings = {
        LogType.Debug : ('debug', logging.DEBUG),
        LogType.Error : ('error', logging.ERROR),
        LogType.Info : ('info', logging.INFO),
        LogType.Warn : ('warn', logging.WARN),
        LogType.Critical : ('critical', logging.CRITICAL),
    }

    @property
    def write_to_console(self) -> bool:
        """!@brief write_to_console boolean property (getter).
        @param self The object pointer.
        @returns True if write to console, else False.
        """
        return self._write_to_console

    @write_to_console.setter
    def write_to_console(self, value) -> None:
        """!@brief write_to_console boolean property (setter).
        @param self The object pointer.
        @param value New value for property.
        @return None
        """
        self._write_to_console = value

    @property
    def external_logger(self) -> str:
        """!@brief external logger function property (getter).
        @param self The object pointer.
        @returns function.
        """
        return self._external_logger

    @external_logger.setter
    def external_logger(self, value):
        """!@brief external logger function property (setter).
        @param self The object pointer.
        @param value New value for property.
        @return None
        """
        self._external_logger = value

    def __init__(self):
        """!@brief Default constructor.
        @param self The object pointer.
        """
        ## External logger function.
        self._external_logger = None
        ## Boolean to specify if logger is initialised.
        self._is_initialised = False
        ## Instance of the internal Python logging system being wrapped.
        self._logger_instance = None
        ## Boolean to specify if writing to the console is enabled.
        self._write_to_console = False

    def initialise(self) -> None:
        """!@brief Initialise the logger.
        @param self The object pointer.
        @return None
        """
        if self._is_initialised:
            raise RuntimeError('Logger is already initialised!')

        logformat= logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                     "%Y-%m-%d %H:%M:%S")

        self._logger_instance = logging.getLogger('system log')
        console_stream = logging.StreamHandler()
        console_stream.setFormatter(logformat)
        self._logger_instance.setLevel(logging.DEBUG)
        self._logger_instance.addHandler(console_stream)

        self._is_initialised = True

    def log(self, log_level, msg, *args) -> None:
        """!@brief Log a message using the logger.
        @param self The object pointer.
        @param log_level Level of the logged message, e.g. debug.
        @param msg Actual message to log.
        @param args Variable arguments used in the message.
        @return None
        """
        if not self._is_initialised:
            raise RuntimeError('Logger is not initialised!')

        if self._write_to_console:
            mapped_method, _ = self.Logger_mappings[log_level]
            method_to_call = getattr(self._logger_instance, mapped_method)
            method_to_call(msg, *args)

        if self._external_logger:
            current_time = time.time()
            compiled_msg = msg % args
            self._external_logger.add_log_event(current_time, log_level,
                                                compiled_msg)
