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
import time
from uuid import uuid1
import sqlite3

class DbInterface:
    """ Wrappinf of Sqlite database functionality """
    __slots__ = ['_connection', '_database_filename', '_is_connected',
                 '_last_error_msg']

    ## Link type can be:
    ## 0 - New
    ## 1 - Rescan
    sql_create_url_queue_table = """
        CREATE TABLE IF NOT EXISTS url_queue (
            id integer PRIMARY KEY,
            url text NOT NULL,
            insertion_date integer NOT NULL,
            cached boolean DEFAULT false,
            task_id varchar(36) NOT NULL,
            link_type integer NOT NULL
        )
    """

    sql_index_url_queue = "CREATE UNIQUE INDEX idx_queue_url ON url_queue(url)"

    @property
    def is_connected(self) -> bool:
        """!@brief Is connected (Getter).
        @param self The object pointer.
        @returns boolean if connected or not.
        """
        return self._is_connected and self._connection is not None

    @property
    def last_error_message(self) -> str:
        """!@brief Last error message (Getter).
        @param self The object pointer.
        @returns Last error message string or empty string if none.
        """
        return self._last_error_msg

    def __init__(self, database_filename):
        """!@brief Class constructor.
        @param self The object pointer.
        @param database_filename Filename and path of the database.
        @returns SqliteInterface instance.
        """

        self._connection = None
        self._database_filename = database_filename
        self._last_error_msg = ''
        self._is_connected = False

    def database_exists(self) -> bool:
        """!@brief Check to see if the database exists.  We verify that:
                   a) The file exist.
                   b) It's at least 100 bytes (min size of header).
                   c) Contains the expected header string.
        @param self The object pointer.
        @returns True if valid, False = not valid.
        """

        if not os.path.isfile(self._database_filename):
            return False

        # SQLite database file header is 100 bytes
        if os.path.getsize(self._database_filename) < 100:
            return False

        with open(self._database_filename, 'rb') as handle:
            header = handle.read(100)

        return header[:16] == b'SQLite format 3\x00'

    def build_database(self) -> bool:
        """!@brief Build a new, empty database ready for use.  The build
                   process closes the database at the end.
        @param self The object pointer.
        @returns Boolean indicating success status.
        """

        self._last_error_msg = ''

        if os.path.isfile(self._database_filename):
            self._last_error_msg = 'file with name already exists!'
            return False

        try:
            self._connection = sqlite3.connect(self._database_filename)

        except sqlite3.OperationalError as op_except:
            self._last_error_msg = f'Database build failed: {str(op_except)}'
            return False

        cursor = self._connection.cursor()

        try:
            cursor.execute(self.sql_create_url_queue_table)

        except sqlite3.Error as mysqlite_exception:
            self._last_error_msg = "Failed to create the 'url_queue' " + \
                f"table, reason: {str(mysqlite_exception)}"
            cursor.close()
            self._connection.close()
            return False

        try:
            cursor.execute(self.sql_index_url_queue)

        except sqlite3.Error as mysqlite_exception:
            self._last_error_msg = "Failed to create index for " + \
                f"'url_queue' table, reason: {str(mysqlite_exception)}"
            cursor.close()
            self._connection.close()
            return False

        cursor.close()
        self._connection.close()
        return True

    def open(self) -> bool:
        """!@brief Open a database and store connection for later use.
        @param self The object pointer.
        @returns Boolean indicating success status.
        """

        try:
            self._connection = sqlite3.connect(self._database_filename)
            cursor = self._connection.cursor()
            cursor.execute('SELECT id FROM url_queue LIMIT 1')

        except sqlite3.Error as sqlite_except:
            self._last_error_msg = f'open failed, reason: {sqlite_except}'
            self._connection = None
            return False

        self._is_connected = True

        return True

    def close(self) -> None:
        """!@brief Close the connection.
        @param self The object pointer.
        @returns None.
        """
        if self._connection:
            self._connection.close()

        self._connection = None

    def get_queue_cache(self, cache_size, get_cached=False) -> list:
        """!@brief Get queue for caching purposes.
        @param self The object pointer.
        @param cache_size Get max number of items to cache.
        @param existing_ids List of items to not get, default is None.
        @returns List of data rows stored in a dictionary.
        """

        if not self._connection:
            raise RuntimeError('No connection')

        cache_clause = 'WHERE NOT cached' if not get_cached else ''

        query = f"SELECT * FROM url_queue {cache_clause} ORDER BY " + \
             f"insertion_date ASC LIMIT {cache_size}"

        cursor = self._connection.cursor()

        column_names = []

        try:
            cursor.execute(query)
            column_names = list(map(lambda x: x[0], cursor.description))

        except sqlite3.Error as sqlite_except:
            raise RuntimeError(f'Query failed, reason: {sqlite_except}') from \
                sqlite_except

        rows = cursor.fetchall()

        data = []

        for row in rows:
            entry = {}

            for idx, column in enumerate(row):
                entry[column_names[idx]] = column

            data.append(entry)

        return data

    def set_ids_to_cached(self, id_list) -> None:
        """!@brief Update entries to be flagged as caching.
        @param self The object pointer.
        @param id_list List of id entries to be flagged.
        @returns None
        """

        if not self._connection:
            raise RuntimeError('No connection')

        id_list = ','.join([str(id) for id in id_list])
        query = f"UPDATE url_queue SET cached = 1 WHERE id IN ({id_list})"
        cursor = self._connection.cursor()

        try:
            cursor.execute(query)
            self._connection.commit()

        except sqlite3.Error as sqlite_except:
            raise RuntimeError(f'Query failed, reason: {sqlite_except}') from \
                sqlite_except

    def add_url(self, url, task_type) -> None:
        """!@brief Add a url to the processing queue database.
        @param self The object pointer.
        @param url URL to be processed.
        @param task_type Task type e.g new or rescan.
        @returns None
        """

        insert_time = round(time.time())
        task_id = str(uuid1())
        task_type_id = 0 if task_type == 'New' else 1

        query = "INSERT INTO url_queue(url, insertion_date, cached, " + \
            f"task_id, link_type) VALUES(\"{url}\", {insert_time}, 0, " + \
            f"{task_id}\", {task_type_id})"

        cursor = self._connection.cursor()

        try:
            cursor.execute(query)
            self._connection.commit()

        except sqlite3.Error as sqlite_except:
            raise RuntimeError(f'Query failed, reason: {sqlite_except}') from \
                sqlite_except
