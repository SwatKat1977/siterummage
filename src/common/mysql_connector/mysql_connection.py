import mysql.connector


class MySQLConnection:
    #spylint: disable=R0914, R0201

    ## \brief Default constructor
    # Default constructor for MySQLConnection class instance.
    # \param self Self reference.
    # \param connPool MySQL Connection object.
    def __init__(self, connection):
        self._connection = connection

    ## \brief Call a MySQL Stored procedure.  A ResultsSet is returned
    # Call a MySQL Stored procedure.  A ResultsSet is returned, if nothing is
    # returned then it's empty.
    # \param self Self reference.
    # \param procedureName Name of the procedure to call.
    # \param params A list of parameters for the stored procedures.
    def call_stored_procedure(self, procedure_name, params=(),
                              keep_conn_alive=False):
        cursor = self._connection.cursor()

        try:
            cursor.callproc(procedure_name, params)

        # It's important to check for exceptions here, which include errors in
        # the query or invalid tables/columns.
        except mysql.connector.errors.ProgrammingError as mysqlExcept:
            self._close(cursor)
            return (None, mysqlExcept.msg)

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
        for fieldName in field_names:
            field_names_map[field_position] = fieldName
            field_position += 1

        results_set = self._build_results(field_names_map, result_rows)
        if not keep_conn_alive:
            self._close(cursor)

        return (results_set, '')


    ## \brief Execute a MySQL query.  A ResultsSet is returned
    # Execute a MySQL SQL query.  A ResultsSet is returned, if nothing is
    # returned then it's empty.
    # \param self Self reference.
    # \param query SQL query to be executed.
    # \param variables A list of parameters for query.
    # \param commit Should query be committed.  Not default for MySQL.
    def query(self, query, variables=(), commit=False, keep_conn_alive=False):
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
        except mysql.connector.errors.ProgrammingError as mysqlExcept:
            self._close(cursor)
            return (None, mysqlExcept.msg)

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

    ## \brief Method to release connection, not actually close it.
    # Method to release connection back into the pool (not actually close it)
    # and clean up the cursor object.
    # \param self Self reference.
    # \param connection Connection to release.
    # \param cursor Cursor object to clean up.
    def _close(self, cursor):
        print('close')
        cursor.close()
        self._connection.close()

    def _build_results(self, column_headers, results):
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
