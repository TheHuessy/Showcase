from SQLEngine import SQLEngine
import os
import pandas as pd
import yaml
import sqlalchemy

class SQLUtils:
    """
    A class to easily send sql commands to a sql database
    """

    def __init__(self,db):
        """
        Initializes the class, fetches user credentials, and passes
        the user specified database to connect to.

        Parameters
        ----------
        db : string
            The name of the database to connect to.

        Returns
        ----------
        self.creds : dict
            A dictionary of credential information.

        self.db : string
            The name of the database to connect to.
        """

        with open(os.environ['CREDS_PATH']) as file:
            self.creds = yaml.full_load(file)
        self.db = db

    def select_query_builder(self, table_name, cols=None, limit_value=None, where_col=None, where_value=None, where_equal=None):
        """
        Builds a SELECT query using user inputs.

        Parameters
        ----------
        table_name : string
            The name of the table to query.

        cols : array[string]
            An array of column names to return in the query. If 
            not specified, the query will assume all columns
            are to be returned.

        limit_value : integer
            The number of lines to limit the query results to. If
            not specified, the query will assume all rows are to 
            be returned.

        where_col : string
            The conditional column name to be specified in a WHERE clause.
            If not specified, then no WHERE clause will be generated. This
            method is not currently set up for multiple WHERE clause conditions.

        where_value : string
            The value of the where_col that will trip the WHERE clause condition.

        where_equal : string
            The operator for the WHERE condition.

        Returns
        ----------
        output_statment : string
            The fully generated SELECT statement.
        """

        limit_clause = "LIMIT {}".format(limit_value) if limit_value else None

        cols = ", ".join(cols) if cols else "*"

        where_clause = "WHERE {} {} '{}'".format(where_col, where_equal, where_value) if where_col else None

        statement = ["SELECT {} FROM {}".format(cols, table_name)]
        statement += [where_clause] if where_clause else ""
        statement += [limit_clause] if limit_clause else ""

        output_statement = " ".join(statement)

        return(output_statement)

    def update_query_builder(self, table_name, update_col, update_value, where_col=None, where_value=None, where_equal=None):
        """
        Builds an UPDATE statement using user inputs.

        Parameters
        ----------
        table_name : string
            The name of the table to query.

        update_col : string
            The column to be updated.

        update_value : string
            The new value that will be updated in the update_col.

        where_col : string
            The conditional column name to be specified in a WHERE clause.
            If not specified, then no WHERE clause will be generated. This
            method is not currently set up for multiple WHERE clause conditions.

        where_value : string
            The value of the where_col that will trip the WHERE clause condition.

        where_equal : string
            The operator for the WHERE condition.

        Returns
        ----------
        output_statment : string
            The fully generated UPDATE statement.
        """

        where_clause = "WHERE {} {} '{}'".format(where_col, where_equal, where_value) if where_col else None
        statement = ["UPDATE {} SET {} = {}".format(table_name, update_col, update_value)]
        statement += [where_clause] if where_clause else ""

        output_statement = " ".join(statement)

        return(output_statement)

    def delete_query_builder(self, table_name, where_col, where_value, where_equal=None):
        """
        Builds a DELETE statement using user inputs.

        Parameters
        ----------
        table_name : string
            The name of the table to query.

        where_col : string
            The conditional column name to be specified in a WHERE clause.

        where_value : string
            The value of the where_col that will trip the WHERE clause condition.

        where_equal : string
            The operator for the WHERE condition.

        Returns
        ----------
        output_statment : string
            The fully generated DELETE statement.
        """

        where_eq = where_equal if where_equal else "="
        where_clause = "WHERE {} {} '{}'".format(where_col, where_eq, where_value)
        statement = ["DELETE FROM {}".format(table_name)]
        statement += [where_clause]

        output_statement = " ".join(statement)

        return(output_statement)


    def get(self, table_name, cols=None, limit_value=None, where_col=None, where_value=None, where_equal=None):
        """
        Exeutes a generated SELECT query using user inputs.
        Returns the resulting data as a pandas dataframe.

        Parameters
        ----------
        table_name : string
            The name of the table to query.

        cols : array[string]
            An array of column names to return in the query. If 
            not specified, the query will assume all columns
            are to be returned.

        limit_value : integer
            The number of lines to limit the query results to. If
            not specified, the query will assume all rows are to 
            be returned.

        where_col : string
            The conditional column name to be specified in a WHERE clause.
            If not specified, then no WHERE clause will be generated. This
            method is not currently set up for multiple WHERE clause conditions.

        where_value : string
            The value of the where_col that will trip the WHERE clause condition.

        where_equal : string
            The operator for the WHERE condition.

        Returns
        ----------
        results : pandas dataframe
            The data returned by the SELECT query.
        """

        query = self.select_query_builder(table_name=table_name, cols=cols, limit_value=limit_value, where_col=where_col, where_value=where_value, where_equal=where_equal)

        print(query)

        with SQLEngine(self.db) as sql_engine:
            result = pd.read_sql(query, sql_engine.engine)

        return(result)

    def update(self, table_name, update_col, update_value, where_equal=None, where_col=None, where_value=None):
        """
        Executes an UPDATE statement using user inputs.

        Parameters
        ----------
        table_name : string
            The name of the table to query.

        update_col : string
            The column to be updated.

        update_value : string
            The new value that will be updated in the update_col.

        where_col : string
            The conditional column name to be specified in a WHERE clause.
            If not specified, then no WHERE clause will be generated. This
            method is not currently set up for multiple WHERE clause conditions.

        where_value : string
            The value of the where_col that will trip the WHERE clause condition.

        where_equal : string
            The operator for the WHERE condition.

        Returns
        ----------
        results : string
            The output confirmation from the statement execution.
        """

        query = self.update_query_builder(table_name=table_name, update_col=update_col, update_value=update_value, where_col=where_col, where_value=where_value, where_equal=where_equal)

        print(query)

        with SQLEngine(self.db) as sql_engine:
            result = sql_engine.execute(query)

        return(result)


    def remove_data(self, table_name, where_col, where_value, where_equal=None):
        """
        Executes a DELETE statement using user inputs.

        Parameters
        ----------
        table_name : string
            The name of the table to query.

        where_col : string
            The conditional column name to be specified in a WHERE clause.

        where_value : string
            The value of the where_col that will trip the WHERE clause condition.

        where_equal : string
            The operator for the WHERE condition.

        Returns
        ----------
        results : string
            The output confirmation from the statement execution.
        """

        query = self.delete_query_builder(table_name=table_name, where_col=where_col, where_value=where_value, where_equal=where_equal)

        print(query)

        with SQLEngine(self.db) as sql_engine:
            result = sql_engine.execute(query)

        return(result)

    def write_dataframe_safe(self,dataframe,dest_table):
        """
        A method to write a user specified dataframe to a SQL database
        with error handling. It is assumed that the data from the
        dataframe will be appended to the destination table if it exists.

        Parameters
        ----------
        dataframe : pandas dataframe
            The dataframe that is to be written to SQL.

        dest_table : string
            The name of the table in the database to write the dataframe to.

        Returns
        ----------
        Writes the dataframe to the database, does not return anything.
        """

        try:
            with SQLEngine(self.db) as engine:
                dataframe.to_sql(
                        name=dest_table,
                        con = engine,
                        if_exists='append',
                        index=False
                        )
        except Exception as err:
            print("Could not write data out to postgres!\n{}".format(err))
        else:
            print("Dataframe written to {}".format(dest_table))

