import os
import yaml
import sqlalchemy


class SQLEngine:
    """
    A simple class to create a context manager for a sqlalchemy connection
    """
    def __init__(self, db):
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

    def conn_string_gen(self, user_name, pw, host):
        """
        Generates a postgres connection string using credential inputs and 
        a user specified database name

        Parameters
        ----------
        user_name : string
            The username credential to access the database.

        pw : string
            The password associated with the user trying to access the database.

        host : string
            The hostname or IP of the Postgres server.

        Returns
        ----------
        output_conn_string : string
            The fully formed connection string used by sqlalchemy.
        """

        output_conn_string = "postgresql+psycopg2://{}:{}@{}/{}".format(user_name, pw, host, self.db)
        return(output_conn_string)

    def __enter__(self):
        """
        Secifies the beginning of the context manager for the class.
        Generates the connection string and opens the connection to
        the database.

        Parameters
        ----------
        None

        Returns
        ----------
        self.engine : SQLAlchemy connection engine object
            The sql connection object used to interact with the databse remotely.
        """

        conn_string = self.conn_string_gen(self.creds['pg_user'], self.creds['pg_pw'], self.creds['pg_host'])
        self.engine = sqlalchemy.create_engine(conn_string)

        return(self.engine)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Specifies what to do when exiting the context manager for this class.
        Ensures that the connection to the sql database is closed before
        exiting the manager.

        Parameters
        ----------
        None, other than inate type, value, and traceback variables.

        Returns
        ----------
        Closes open connection and returns nothing.
        """

        if self.engine:
            self.engine.dispose()

