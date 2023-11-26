import pyodbc

from utils.utils import get_sqlconnection_string


# Funzione per connettersi a un database MySQL
def create_server_connection():
    connection = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:smartapp.database.windows.net,"
                                "1433;DATABASE=kpi_engine;UID=smartapp2324;PWD=Sm4rt4pp2324!")
    return connection


# Funzione per eseguire una query/write query
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except pyodbc.Error as err:
        print(f"Error: '{err}'")
    finally:
        # Chiusura della connessione al database
        connection.close()


# Funzione per eseguire una query di lettura (SELECT)
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        # Chiusura della connessione al database
        connection.close()
        return result
    except pyodbc.Error as err:
        print(f"Error: '{err}'")
    finally:
        # Chiusura della connessione al database
        connection.close()
