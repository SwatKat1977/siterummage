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
from common.logger import Logger, LogType
from common.core_version import CORE_VERSION
from common.service_base import ServiceBase
from .api.node_management import ApiNodeManagement
from .api.schedule import ApiSchedule
from .configuration_manager import ConfigurationManager
from .scrape_node_list import ScrapeNodeList
from .version import VERSION

class Service(ServiceBase):
    """ Siterummage Big Broker microservice class """

    ## Title text logged during initialisation.
    title_text = 'Site Rummagge Big Broker Microservice'

    ## Copyright text logged on initialisation etc.
    copyright_text = 'Copyright 2021 Site Rummage'

    ## License text logged on initialisation etc.
    license_text = 'Licensed under The GNU Public License v3.0'

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

        self._scrape_node_list = ScrapeNodeList()

    def _initialise(self) -> bool:
        self._logger.write_to_console = True
        self._logger.initialise()

        self._logger.log(LogType.Info,
                         f'{self.title_text} {VERSION} (Core Version {CORE_VERSION})')
        self._logger.log(LogType.Info, self.copyright_text)
        self._logger.log(LogType.Info, self.license_text)

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
        self._logger.log(LogType.Info, '+== Page Store Api :->')
        self._logger.log(LogType.Info, f'+= host : {processing_queue_cfg.host}')
        self._logger.log(LogType.Info, f'+= port : {processing_queue_cfg.port}')
        self._logger.log(LogType.Info, '+==============================+')

        self._api_schedule = ApiSchedule(self._quart, self._configuration)

        self._api_node_management = ApiNodeManagement(self._quart,
                                                      self._configuration,
                                                      self._scrape_node_list)

        self._is_initialised = True

        return True

    async def _main_loop(self):
        # if not self._master_thread_class.initialise():
        #     return False
        pass

    def _shutdown(self):
        self._logger.log(LogType.Info, 'Shutting down...')
