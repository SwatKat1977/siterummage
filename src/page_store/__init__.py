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
#pylint: disable=wrong-import-position
import os
import sys
sys.path.insert(0,'.')
from quart import Quart
from .service import Service

## Quart application instance
app = Quart(__name__)

## Page Store microservice instance, this contains the code that is executed
service = Service(app)

@app.before_serving
async def startup() -> None:
    """!@brief Code executed before Quart has began serving http requests.
    @return None
    """
    # app.service_task = asyncio.ensure_future(service.start())
    print('[DEBUG] @app.before_serving')

@app.after_serving
async def shutdown() -> None:
    """!@brief Code executed after Quart has stopped serving http requests.
    @return None
    """
    # service.signal_shutdown_requested()

    # while not service.shutdown_completed:
    #     await asyncio.sleep(0.5)
    print('[DEBUG] @app.after_serving')

if not os.getenv('SITERUMMAGE_PAGESTORE_CONFIG'):
    print('[ERROR] SITERUMMAGE_PAGESTORE_CONFIG environment variable ' + \
                      'is not defined!')
    sys.exit(1)

if not service.initialise():
    sys.exit()
