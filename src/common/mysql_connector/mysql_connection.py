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
import mysql.connector

class MySQLConnection:
    ''' MySQL connection class '''

    def __init__(self, connection) -> object:
        """!@brief Default constructor for MySQLConnection class.
        @param self The object pointer
        @param connection MySQL Connection object
        @returns Constructed MySQLConnection instance.
        """
        self._connection = connection

    def close(self) -> None:
        """!@brief Method to release connection from pool.
        @param self The object pointer
        @returns None
        """
        self._connection.close()

    def call_stored_procedure(self, procedure_name, params=(),
                              keep_conn_alive=False):
        """!@brief Call a MySQL Stored procedure.  A ResultsSet is returned,
            if nothing is returned then it's empty.
        @param self The object pointer
        @param procedure_name Name of the procedure to call
        @param params Optional list of parameters for the stored procedures
        @param keep_conn_alive Optional flag if to keep conneciton alive
        @returns Constructed MySQLConnection instance.
        """

        cursor = self._connection.cursor()

        try:
            cursor.callproc(procedure_name, params)

        # It's important to check for exceptions here, which include errors in
        # the query or invalid tables/columns.
        except mysql.connector.errors.ProgrammingError as mysql_except:
            self._close(cursor)
            return (None, mysql_except.msg)

        results_set = []

        # Get the results from the stored procedure.
        results = cursor.stored_results()

        result_rows = None

        for row in results:
            result_rows = list(row.fetchall())

        if len(result_rows) == 0:
            self._close(cursor)
            return (results_set, 'Missing column title!')

        # Pull out the field names and build a map of there position.
        field_names = list(result_rows.pop(0))
        field_names_map = {}
        field_position = 0
        for field_name in field_names:
            field_names_map[field_position] = field_name
            field_position += 1

        results_set = self._build_results(field_names_map, result_rows)
        if not keep_conn_alive:
            self._close(cursor)

        return (results_set, '')

    def query(self, query, variables=(), commit=False, keep_conn_alive=False):
        """!@brief Execute a MySQL query.  A ResultsSet is returned. A
            ResultsSet is returned, if nothing is returned then it's empty.
        @param self The object pointer.
        @param query SQL query to be executed
        @param variables An optional list of parameters for query
        @param commit Optional flag if query be committed. Default is False
        @param keep_conn_alive Optional flag if to keep conneciton alive
        @returns Tuple (results, error_message)
        """

        cursor = self._connection.cursor()

        try:
            cursor.execute(query, variables)

            if commit is True:
                self._connection.commit()

                if not keep_conn_alive:
                    self._close(cursor)

                return ([], '')

        # It's important to check for exceptions here, which include errors in
        # the query or invalid tables/columns.
        except mysql.connector.errors.ProgrammingError as mysql_exception:
            self._close(cursor)
            return (None, mysql_exception.msg)

        try:
            # Fetch all of the results rows returned from MySQL.
            rows = cursor.fetchall()

            # Pull out the field names and build a map of there position.
            field_names = [i[0] for i in cursor.description]
            field_names_map = {}
            field_position = 0
            for field_name in field_names:
                field_names_map[field_position] = field_name
                field_position += 1

            results_set = self._build_results(field_names_map, rows)

            print(keep_conn_alive)
            if not keep_conn_alive:
                self._close(cursor)

            return (results_set, '')

        # This isn't an exception, we are using it to check if no results are
        # returned (e.g. a query such as UPDATE).
        except mysql.connector.errors.InterfaceError:
            self._close(cursor)
            return ([], '')

    def _close(self, cursor) -> None:
        """!@brief Method to release connection, not actually close it.
        @param self The object pointer
        @param cursor Cursor object to clean up
        @returns None
        """
        cursor.close()
        self._connection.close()

    def _build_results(self, column_headers, results) -> list:
        """!@brief Take the raw results from MySQL and create a user-friendly
            output which is a list of dictionaries.
        @param self The object pointer
        @param column_headers List of column headers
        @param results Raw results from MySQL
        @returns List of dictionaries representing results.
        """
        #pylint: disable=no-self-use

        # The output results set after processing the results.
        results_set = []

        # Iterate through rows getting results back.
        for row in results:

            # A row consists of a dictionary of values in the format of
            # ColumnName : value
            result_row = {}

            # Iterate through columns.
            for column_index, column_name in column_headers.items():
                result_row[column_name] = row[column_index]

            results_set.append(result_row)

        return results_set
