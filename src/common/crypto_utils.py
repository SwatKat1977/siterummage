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
import base64
import typing
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

class CryptoUtils:
    ''' Cryptographic wrapper methods '''
    slots__ = ['_private_key', '_private_key_cipher', '_public_key',
               '_public_key_cipher']

    def __init__(self):
        self._private_key = None
        self._private_key_cipher = None
        self._public_key = None
        self._public_key_cipher = None

    def decrypt(self, encrypted_str, decode_base64=False):
        """!@brief Decrypt a string using the key provided, optionally it can
                   be base64 decoded.
        @param self The object pointer.
        @param encrypted_str String to decrypt.
        @param decode_base64 Flag to base64 decoded.
        @returns decryptedStr, errorStr.
        """

        if not self._private_key:
            raise ValueError('No private key loaded!')

        raw_encrypted_str = encrypted_str

        if decode_base64:
            try:
                raw_encrypted_str = base64.b64decode(encrypted_str)

            except Exception:
                return None, 'bad Base64 encoding'

        try:
            decrypted_str = self._private_key_cipher.decrypt(raw_encrypted_str)

        except ValueError as ex:
            return None, f'Invalid crypto key {ex}'

        return decrypted_str, ''

    def encrypt(self, decrypted_str, encode_base64=False):
        """!@brief Encrypt a string using the key provided, optionally it can
                   be base64 encoded.
        @param self The object pointer.
        @param decrypted_str String to encrypt.
        @param encode_base64 Flag to base64 encode.
        @returns encryptedStr, errorStr.
        """

        if not self._public_key:
            raise ValueError('No public key loaded!')

        raw = str.encode(decrypted_str)

        encrypted_str = self._public_key_cipher.encrypt(raw)

        if encode_base64:
            encrypted_str = base64.b64encode(encrypted_str)
            return encrypted_str.decode('ascii')

        return encrypted_str

    def load_public_key(self, key_filename) -> typing.Tuple[bool, str]:
        """!@brief Attempt to load a public key.
        @param self The object pointer.
        @returns tuple [Boolean : success status, error message if failed].
        """

        try:
            with open(key_filename, 'r') as file_handle:
                file_contents = file_handle.read()

        except FileNotFoundError as io_except:
            err = f"Unable to read public key '{key_filename}', reason: " + \
                str(io_except)
            return False, err

        self._public_key = RSA.import_key(file_contents)
        self._public_key_cipher = PKCS1_OAEP.new(key=self._public_key)

        return True, ''


    def load_private_key(self, key_filename) -> typing.Tuple[bool, str]:
        """!@brief Attempt to load the private key used by Site Rummage.
        @param self The object pointer.
        @returns tuple [Boolean : success status, error message if failed].
        """

        try:
            with open(key_filename, 'r') as file_handle:
                file_contents = file_handle.read()

        except FileNotFoundError as io_except:
            err = f"Unable to read private key '{key_filename}', reason: " + \
                str(io_except)
            return False, err

        self._private_key = RSA.import_key(file_contents)
        self._private_key_cipher = PKCS1_OAEP.new(key=self._private_key)

        return True, ''
