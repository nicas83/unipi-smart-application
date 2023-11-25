import mysql.connector
import os
import json
import random
from datetime import datetime, date

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


def ir(connection, db):
    try:
        if connection.is_connected():
            connection.database = db
            alfa = connection.cursor()
            alfa.execute("USE STORAGE")
            query = "SELECT * FROM KPIS;"
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            rows = cursor.fetchall()

            return json.dumps(rows, cls=MyEncoder)

    except mysql.connector.Error as err:
        print(f"Connection error: {err}")

def show_databases(connection):
    try:
        if connection.is_connected():
            
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES;")

            # Visualizza i risultati
            print("Elenco dei database:")
            for (db,) in cursor:
                print(db)

    except mysql.connector.Error as err:
        print(f"Errore durante l'esecuzione della query: {err}")
        
        
        
def add_kpis(connection, n, db):
    try:
        if connection.is_connected():
            print("Connessione al database riuscita")

            # Seleziona il database
            connection.database = db
            #last kpi name value in the table
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(CAST(SUBSTRING_INDEX(NOME, '_', -1) AS SIGNED)) FROM KPIS;")
            result = cursor.fetchone()
            last_value = result[0] if result[0] is not None else 0

            # insert data
            cursor = connection.cursor()
            for i in range(last_value + 1, last_value + n + 1):
                name = f"Kpi_{i}"
                value = random.uniform(1.0, 100.0)
                data = '2023-01-01'  # Imposta la data su '2023-01-01'

                query = f"INSERT INTO KPIS (NOME, VALORE, DATA) VALUES ('{name}', {value}, '{data}');"
                cursor.execute(query)

            connection.commit()
            print(f"Inserite {n} righe nella tabella KPIS")

    except mysql.connector.Error as err:
        print(f"Errore di connessione al database: {err}")



        
def delete_kpis(connection,db):
    try:
        if connection.is_connected():
       
            connection.database = db
            cursor = connection.cursor()
            cursor.execute("DELETE FROM KPIS;")
            connection.commit()
            print("Righe eliminate dalla tabella KPIS")
            
    except mysql.connector.Error as err:
        print(f"Errore durante l'esecuzione della query: {err}")
                                
def main():
    # connect to the db
    connection = None
    database = os.environ.get("MYSQL_DATABASE")
    user = "root"
    password = "smartapp"
    host = os.environ.get("targetip", "127.0.0.1")
    port = os.environ.get("port", 3306)

    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            print("Connection established")

            # MENU
            choice = int(input("Inserisci 1 per visualizzare i database, 2 per aggiungere KPIs, 3 per vedere i kpis, 4 per eliminare i kpis dal db: "))
            if choice == 1:
                show_databases(connection)
                
            elif choice == 2:
                n = int(input("Inserisci il numero di KPIs da aggiungere: "))
                add_kpis(connection, n, "STORAGE")
                
            elif choice == 3:
                result = ir(connection, "STORAGE")
                print(result)    
                
            elif choice == 4:
                delete_kpis(connection, "STORAGE")    
            else:
                print("Scelta non valida")

    except mysql.connector.Error as err:
        print(f"Errore di connessione al database: {err}")

    finally:
        # Close the session
        if connection and connection.is_connected():
            connection.close()
            print("Connessione al database chiusa")
            
if __name__ == "__main__":
    main()