import requests
from flask import Flask, request, jsonify

from data.mysql_connection import create_server_connection, read_query

app = Flask(__name__)

server = 'tcp:smartapp.database.windows.net,1433'
database = 'kpi_engine'
username = 'smartapp2324'
password = 'Sm4rt4pp2324!'
driver= '{ODBC Driver 17 for SQL Server}'

conn_str = f'DRIVER={driver};Server={server};Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'


@app.route('/', methods=['GET'])
def index():
    return "Hello, World! The group 3 will SUCK!"


@app.route('/kpi_definition', methods=['POST'])
def add_new_kpi_definition():
    # Estrai il JSON dalla richiesta POST
    data = request.get_json()

    # eseguo la chiamata verso le api influx
    url = "http://localhost:8086/add_kpi/"
    response = requests.get(url)
    # Rispondi con il JSON ricevuto da influx
    return response.json()


@app.route('/kpi/<kpi_name>', methods=['GET'])
def get_kpi_by_name(kpi_name):
    try:
        print("getting connection")
        connection = create_server_connection(conn_str)
        print("connection created")
        query = "SELECT * FROM KPI_CATALOGUE WHERE kpi_name = %s" + kpi_name + "ORDER BY date DESC LIMIT 1"
        result = read_query(connection, query)

        # creo il json da restituire al FE
        kpis = [{"kpi_name": row[0], "value": row[1], "date": row[2]} for row in result]

        return jsonify(kpis)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred retrieving the KPIs."}), 500


@app.route('/kpis', methods=['GET'])
def get_all_kpi():
    try:
        connection = create_server_connection()
        query = "SELECT * FROM KPI_CATALOGUE ORDER BY date DESC LIMIT 1"
        result = read_query(connection, query)

        # creo il json da restituire al FE
        kpis = [{"kpi_name": row[0], "value": row[1], "date": row[2]} for row in result]

        return jsonify(kpis)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred retrieving the KPIs."}), 500


if __name__ == '__main__':
    app.run(debug=True)
