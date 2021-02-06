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
#pylint: disable=wrong-import-position
import asyncio
import os
import sys
sys.path.insert(0,'.')
from quart import Quart
from .service import Service

## Quart application instance
app = Quart(__name__)

## Microservice instance, this contains the code that is executed
service = Service(app)

@app.before_serving
async def startup() -> None:
    """!@brief Code executed before Quart has began serving http requests.
    @return None
    """
    app.service_task = asyncio.ensure_future(service.start())

@app.after_serving
async def shutdown() -> None:
    """!@brief Code executed after Quart has stopped serving http requests.
    @return None
    """
    service.signal_shutdown_requested()

    while not service.shutdown_completed:
        await asyncio.sleep(0.5)

if not os.getenv('SITERUMMAGE_PROCESSINGQUEUE_CONFIG'):
    print('[ERROR] SITERUMMAGE_PROCESSINGQUEUE_CONFIG environment variable' + \
                      ' is not defined!')
    sys.exit(1)

if not service.initialise():
    sys.exit()
