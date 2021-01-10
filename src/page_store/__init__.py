#pylint: disable=wrong-import-position
import sys
sys.path.insert(0,'.')
from common.mysql_connector.mysql_adaptor import MySQLAdaptor

from quart import Quart

## Quart application instance
app = Quart(__name__)

mysql_adaptor = MySQLAdaptor('root', 'siterummage', '127.0.0.1', 4000, pool_size=1)

foo = mysql_adaptor.connect('master_2021')
print(foo.call_stored_procedure('g'))

foo = mysql_adaptor.connect('master_2021')
print('2nd conn', foo)
query = "INSERT INTO domain(id, name) VALUES(0, 'https://www.test.com')"

print(foo.query(query, commit=True))
foo = mysql_adaptor.connect('master_2021')
print(foo.query('SELECT * FROM domain'))