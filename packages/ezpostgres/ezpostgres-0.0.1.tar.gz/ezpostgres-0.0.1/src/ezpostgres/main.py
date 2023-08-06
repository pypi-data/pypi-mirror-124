"""
Owner: Kevin B
Contributors: N/A
Date Created: 2021-10-23

Summary:
    Wrapper around psycopg2 for postgres.

"""
############################# IMPORTS #############################


# From PYPI
import psycopg2



############################# CLASS #############################
class Ezpostgres():
    """Wrapper around psycopg2 for postgres. This was made for a lazy person to
    quickly use postgres via Python.
    """

    def __init__(self, host, dbname, username, password, port=5432, auto_connect=True) -> None:
        """[summary]

        Args:
            host ([type]): [description]
            dbname ([type]): [description]
            username ([type]): Username to sign in to database
            password ([type]): Password to sign in to database
            port (int, optional): Port used to connect to postgres. Defaults to 5432.
            auto_connect (bool, optional): Will return a connection upon initialization. Defaults to True.
        """
        self.host = host
        self.dbname = dbname
        self.username = username
        self.password = password
        self.port = port
        self.auto_connect = auto_connect

    @classmethod
    def from_connection_string(cls, connection_string):
        pass


    ############################# PUBLIC  #############################








    ############################# PRIVATE  #############################


