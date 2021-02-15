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
import os
from Crypto.PublicKey import RSA
from common.logger import Logger, LogType
from common.info import BUILD_NO, COPYRIGHT_TEXT, CORE_VERSION, LICENSE_TEXT
from common.service_base import ServiceBase
from .api.node_management import ApiNodeManagement
from .api.schedule import ApiSchedule
from .api.task import ApiTask
from .configuration_manager import ConfigurationManager
from .scrape_node_list import ScrapeNodeList

class Service(ServiceBase):
    #pylint: disable=too-many-instance-attributes
    """ Siterummage Big Broker microservice class """

    ## Title text logged during initialisation.
    title_text = 'Site Rummagge Big Broker Microservice'

    def __init__(self, new_instance):
        super().__init__()

        self._quart = new_instance

        ## Instance of the logging wrapper class
        self._logger = Logger()

        ## _is_initialised is inherited from parent class ServiceThread
        self._is_initialised = False

        self._configuration = None

        self._api_schedule = None

        self._api_node_management = None

        self._api_task = None

        self._scrape_node_list = ScrapeNodeList()

        self._private_key = ''

    def _initialise(self) -> bool:
        self._logger.write_to_console = True
        self._logger.initialise()

        self._logger.log(LogType.Info, f'{self.title_text} {CORE_VERSION}' + \
                         f'-{BUILD_NO}')
        self._logger.log(LogType.Info, COPYRIGHT_TEXT)
        self._logger.log(LogType.Info, LICENSE_TEXT)

        config_mgr = ConfigurationManager()

        config_file = os.getenv('SITERUMMAGE_BIGBROKER_CONFIG')

        self._logger.log(LogType.Info, f'Configuration file: {config_file}')

        self._configuration = config_mgr.parse_config_file(config_file)
        if not self._configuration:
            self._logger.log(LogType.Error, config_mgr.last_error_msg)
            return False

        self._logger.log(LogType.Info, '+=== Configuration Settings ===+')
        self._logger.log(LogType.Info, '+==============================+')
        page_store_cfg = self._configuration.page_store_api
        self._logger.log(LogType.Info, '+== Page Store Api :->')
        self._logger.log(LogType.Info, f'+= host : {page_store_cfg.host}')
        self._logger.log(LogType.Info, f'+= port : {page_store_cfg.port}')
        processing_queue_cfg = self._configuration.processing_queue_api
        self._logger.log(LogType.Info, '+== Processing Store Api :->')
        self._logger.log(LogType.Info, f'+= host : {processing_queue_cfg.host}')
        self._logger.log(LogType.Info, f'+= port : {processing_queue_cfg.port}')
        self._logger.log(LogType.Info, '+==============================+')
        big_broker_cfg = self._configuration.big_broker_api
        self._logger.log(LogType.Info, '+== Big Broker Api :->')
        self._logger.log(LogType.Info,
                         f'+= Private Key file : {big_broker_cfg.private_key}')

        self._api_schedule = ApiSchedule(self._quart, self._configuration)

        if not self._load_private_key():
            return False

        self._api_node_management = ApiNodeManagement(self._quart,
                                                      self._configuration,
                                                      self._scrape_node_list,
                                                      self._logger,
                                                      self._private_key)

        self._api_task = ApiTask(self._quart, self._configuration,
                                 self._logger)

        self._is_initialised = True

        return True

    async def _main_loop(self):
        # if not self._master_thread_class.initialise():
        #     return False
        pass

    def _shutdown(self):
        self._logger.log(LogType.Info, 'Shutting down...')

    def _load_private_key(self) -> bool:
        """!@brief Attempt to load the private key used by Site Rummage.
        @param self The object pointer.
        @returns Boolean : True = success, False = failed.
        """

        key_filename = self._configuration.big_broker_api.private_key

        try:
            with open(key_filename, 'r') as file_handle:
                file_contents = file_handle.read()

        except FileNotFoundError as io_except:
            err = f"Unable to read private key '{key_filename}', reason: " + \
                str(io_except)
            self._logger.log(LogType.Critical, err)
            return False

        self._private_key = RSA.import_key(file_contents)

        self._logger.log(LogType.Info, 'Private PKI key loaded...')

        return True
