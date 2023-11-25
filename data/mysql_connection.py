import mysql.connector
#from mysql.connector import Error

from utils.utils import config_mysql_parser


# Funzione per connettersi a un database MySQL
def create_server_connection():
    config = config_mysql_parser('config/mysql.properties')
    connection = None
    # try:
    #     connection = mysql.connector.connect(
    #         host=config["hostname"],
    #         user=config["username"],
    #         passwd=config["password"],
    #         database=config["database"]
    #     )
    #     print("MySQL Database connection successful")
    # except Error as err:
    #     print(f"Error: '{err}'")
    return connection


# Funzione per eseguire una query/write query
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
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
    except Error as err:
        print(f"Error: '{err}'")
