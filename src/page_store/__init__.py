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
import sys
sys.path.insert(0,'.')
from common.mysql_connector.mysql_adaptor import MySQLAdaptor

from quart import Quart

## Quart application instance
app = Quart(__name__)


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

# if not service.initialise():
#     sys.exit()

mysql_adaptor = MySQLAdaptor('root', 'siterummage', '127.0.0.1', 4000, pool_size=1)

foo = mysql_adaptor.connect('master_2021')
print(foo.call_stored_procedure('g'))

foo = mysql_adaptor.connect('master_2021')
print('2nd conn', foo)
query = "INSERT INTO domain(id, name) VALUES(0, 'https://www.test.com')"

print(foo.query(query, commit=True))
foo = mysql_adaptor.connect('master_2021')
print(foo.query('SELECT * FROM domain'))