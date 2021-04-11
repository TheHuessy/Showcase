from SQLEngine import SQLEngine
import os
import pandas as pd
import yaml
import sqlalchemy

class SQLUtils:

    def __init__(self,db):
        with open(os.environ['CREDS_PATH']) as file:
            self.creds = yaml.full_load(file)
        self.db = db

    def select_query_builder(self, table_name, cols=None, limit_value=None, where_col=None, where_value=None, where_equal=None):

        limit_clause = "LIMIT {}".format(limit_value) if limit_value else None

        cols = ", ".join(cols) if cols else "*"

        where_clause = "WHERE {} {} '{}'".format(where_col, where_equal, where_value) if where_col else None

        statement = ["SELECT {} FROM {}".format(cols, table_name)]
        statement += [where_clause] if where_clause else ""
        statement += [limit_clause] if limit_clause else ""

        output_statement = " ".join(statement)

        return(output_statement)

    def update_query_builder(self, table_name, update_col, update_value, where_col=None, where_value=None, where_equal=None):
        where_clause = "WHERE {} {} '{}'".format(where_col, where_equal, where_value) if where_col else None
        statement = ["UPDATE {} SET {} = {}".format(table_name, update_col, update_value)]
        statement += [where_clause] if where_clause else ""

        output_statement = " ".join(statement)

        return(output_statement)

    def delete_query_builder(self, table_name, where_col, where_value, where_equal=None):
        where_eq = where_equal if where_equal else "="
        where_clause = "WHERE {} {} '{}'".format(where_col, where_eq, where_value)
        statement = ["DELETE FROM {}".format(table_name)]
        statement += [where_clause]

        output_statement = " ".join(statement)

        return(output_statement)


    def get(self, table_name, cols=None, limit_value=None, where_col=None, where_value=None, where_equal=None):
        query = self.select_query_builder(table_name=table_name, cols=cols, limit_value=limit_value, where_col=where_col, where_value=where_value, where_equal=where_equal)

        print(query)

        with SQLEngine(self.db) as sql_engine:
            result = pd.read_sql(query, sql_engine.engine)

        return(result)

    def update(self, table_name, update_col, update_value, where_equal=None, where_col=None, where_value=None):
        query = self.update_query_builder(table_name=table_name, update_col=update_col, update_value=update_value, where_col=where_col, where_value=where_value, where_equal=where_equal)

        print(query)

        with SQLEngine(self.db) as sql_engine:
            result = sql_engine.execute(query)

        return(result)


    def remove_data(self, table_name, where_col, where_value, where_equal=None):
        query = self.delete_query_builder(table_name=table_name, where_col=where_col, where_value=where_value, where_equal=where_equal)

        print(query)

        with SQLEngine(self.db) as sql_engine:
            result = sql_engine.execute(query)

        return(result)

    def write_dataframe_safe(self,dataframe,dest_table):
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

