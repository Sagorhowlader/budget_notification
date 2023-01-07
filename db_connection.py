import mysql.connector


class Database:
    def __init__(self, host, user, password, database):
        """
        Initialize the database connection and cursor.

        Parameters:
        - host: the hostname of the database server
        - user: the username to connect to the database
        - password: the password for the user
        - database: the name of the database to connect to
        """
        self.database = database
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
        print(f"Successfully connected to {database} database")

    def close(self):
        """
        Close the database connection.
        """
        self.connection.close()
        print(f"Connection to {self.database} closed")

    def execute(self, query: str, values=None):
        """
        Execute a query(Insert or Update).
        """
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return "Query successfully executed"
        except Exception as e:
            print("Error: Unable to execute query")
            print("Error message:", e)
            return None

    def fetch_all(self, query: str, values=None):
        """
        Fetch all rows resulting from a SELECT query.
        """
        try:
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print("Error: Unable to retrieve data from the database.")
            print("Error message:", e)
            return None
