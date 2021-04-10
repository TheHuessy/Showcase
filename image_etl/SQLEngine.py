import os
import yaml
import sqlalchemy


class SQLEngine:

    def conn_string_gen(self, user_name, pw, host):
        output_conn_string = "postgresql+psycopg2://{}:{}@{}/{}".format(user_name, pw, host, self.db)
        return(output_conn_string)

    def __init__(self, db):
        with open(os.environ['CREDS_PATH']) as file:
            self.creds = yaml.full_load(file)
        self.db = db

    def __enter__(self):
        conn_string = self.conn_string_gen(self.creds['pg_user'], self.creds['pg_pw'], self.creds['pg_host'])
        self.engine = sqlalchemy.create_engine(conn_string)

        return(self.engine)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.engine:
            self.engine.dispose()

