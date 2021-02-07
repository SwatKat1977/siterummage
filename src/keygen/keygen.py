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
import sys
sys.path.insert(0,'.')
from Crypto.PublicKey import RSA
from common.logger import Logger, LogType

logger = Logger()
logger.write_to_console = True
logger.initialise()

logger.log(LogType.Info, 'Site Rummagge PKI Key Generator')
logger.log(LogType.Info, 'Copyright 2021 Site Rummage')
logger.log(LogType.Info, 'Licensed under The GNU Public License v3.0')

logger.log(LogType.Info, 'Generating 4096 bit private key...')
private_key = RSA.generate(4096)
logger.log(LogType.Info, 'Private key generated')

logger.log(LogType.Info, 'Generating public key from private key...')
public_key = private_key.publickey()
logger.log(LogType.Info, 'Public key generated')

#Converting the RsaKey objects to string
private_pem = private_key.export_key().decode()
public_pem = public_key.export_key().decode()

logger.log(LogType.Info, 'Writing private key to file (private_key.pem)')
with open('private_key.pem', 'w') as pr:
    pr.write(private_pem)

logger.log(LogType.Info, 'Writing public key to file (private_key.pem)')
with open('public_key.pem', 'w') as pu:
    pu.write(public_pem)

logger.log(LogType.Info, 'Done...')
