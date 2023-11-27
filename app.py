from datetime import datetime
import random

import requests
from flask import Flask, request, jsonify

from data.mysql_connection import create_server_connection, read_query

app = Flask(__name__)
kpis = [
    {"kpi_name": "oee", "value": 10.2, "taxonomy": "PRODUCTION", "group_by": "ALL",
     "last_update": "2023-11-23T00:00:00.000Z"},
    {"kpi_name": "av", "value": 5, "taxonomy": "PRODUCTION", "group_by": "ALL",
     "last_update": "2023-11-24T00:00:00.000Z"},
    {"kpi_name": "aq", "value": 3.7, "taxonomy": "PRODUCTION", "group_by": "ALL",
     "last_update": "2023-11-25T00:00:00.000Z"},
    {"kpi_name": "pe", "value": 0.7, "taxonomy": "PRODUCTION", "group_by": "ALL",
     "last_update": "2023-11-25T00:00:00.000Z"},
    {"kpi_name": "production_volume", "value": 200, "taxonomy": "PRODUCTION", "group_by": "ALL",
     "last_update": "2023-11-25T00:00:00.000Z"},
    {"kpi_name": "downtime_rate", "value": 0.7, "taxonomy": "PRODUCTION", "group_by": "ALL",
     "last_update": "2023-11-25T00:00:00.000Z"},
    {"kpi_name": "energy_consumption", "value": 320.7, "taxonomy": "PRODUCTION", "group_by": "ALL",
     "last_update": "2023-11-25T00:00:00.000Z"}
]


@app.route('/', methods=['GET'])
def index():
    return "Hello, World! This is the SmartApp Kpi Engine project!"


@app.route('/kpi_definition', methods=['POST'])
def add_new_kpi_definition():
    # Estrai il JSON dalla richiesta POST
    data = request.get_json()

    # eseguo la chiamata verso le api influx
    url = "http://localhost:8086/add_kpi/"
    response = requests.get(url)
    # Rispondi con il JSON ricevuto da influx
    return response.json()


@app.route('/kpi', methods=['POST'])
def add_new_kpi():
    # Estrai il JSON dalla richiesta POST
    data = request.get_json()

    # Estrai i campi specifici
    name = data.get('name').upper()
    taxonomy = data.get('taxonomy').upper()
    group_by = data.get('group_by').upper()

    # Genera un valore casuale e ottieni il timestamp corrente
    value = round(random.uniform(1, 30), 2)
    last_update = datetime.now().isoformat() + 'Z'

    # Crea un nuovo KPI e aggiungilo alla lista globale
    new_kpi = {
        "kpi_name": name,
        "taxonomy": taxonomy,
        "group_by": group_by,
        "value": value,
        "last_update": last_update
    }
    kpis.append(new_kpi)

    # Ritorna una risposta JSON
    return jsonify({"message": "KPI added successfully", "new_kpi": new_kpi})


@app.route('/kpi/<kpi_name>', methods=['GET'])
def get_kpi_by_name(kpi_name):
    try:
        # print("getting connection") # connection = create_server_connection(conn_str) print("connection created")
        # query = "SELECT * FROM KPI_CATALOGUE WHERE kpi_name = %s" + kpi_name.upper() + "ORDER BY last_update DESC
        # LIMIT 1" # result = read_query(connection, query)
        #
        # # creo il json da restituire al FE
        # # kpis = [{"kpi_name": row[0], "value": row[1], "last_update": row[2]} for row in result]


        # Cerca il KPI corrispondente nel dizionario
        kpi = next((item for item in kpis if item["kpi_name"].upper() == kpi_name.upper()), None)

        # Se il KPI è trovato, restituiscilo
        if kpi:
            return jsonify(kpi)
        else:
            # Se il KPI non è trovato, restituisci un messaggio di errore
            return jsonify({"error": "KPI not found"}), 404

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred retrieving the KPIs."}), 500


@app.route('/kpis', methods=['GET'])
def get_all_kpi():
    try:
        # connection = create_server_connection()
        query = "SELECT * FROM KPI_CATALOGUE ORDER BY last_update DESC LIMIT 1"
        # result = read_query(connection, query)

        # creo il json da restituire al FE
        # kpis = [{"kpi_name": row[0], "value": row[1], "last_update": row[2]} for row in result]
        # kpis = [
        #     {"kpi_name": "OEE", "value": 10.2, "taxonomy": "", "group_by": "",
        #      "last_update": "2023-11-23T00:00:00.000Z"},
        #     {"kpi_name": "AV", "value": 5, "taxonomy": "", "group_by": "", "last_update": "2023-11-24T00:00:00.000Z"},
        #     {"kpi_name": "AQ", "value": 3.7, "taxonomy": "", "group_by": "", "last_update": "2023-11-25T00:00:00.000Z"},
        #     {"kpi_name": "PE", "value": 0.7, "taxonomy": "", "group_by": "", "last_update": "2023-11-25T00:00:00.000Z"},
        #     {"kpi_name": "PRODUCTION_VOLUME", "value": 200, "taxonomy": "", "group_by": "",
        #      "last_update": "2023-11-25T00:00:00.000Z"},
        #     {"kpi_name": "DOWNTIME_RATE", "value": 0.7, "taxonomy": "", "group_by": "",
        #      "last_update": "2023-11-25T00:00:00.000Z"},
        #     {"kpi_name": "ENERGY_CONSUMPTION", "value": 320.7, "taxonomy": "", "group_by": "",
        #      "last_update": "2023-11-25T00:00:00.000Z"},
        #     {"kpi_name": "AHA", "value": 10.7, "taxonomy": "", "group_by": "",
        #      "last_update": "2023-11-25T00:00:00.000Z"},
        #     {"kpi_name": "EH", "value": 10.7, "taxonomy": "", "group_by": "", "last_update": "2023-11-25T00:00:00.000Z"}
        # ]

        return jsonify(kpis)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred retrieving the KPIs. Error:{e}"}), 500


def get_kpi_stats(taxonomy=None):
    if taxonomy is None or taxonomy.upper() == 'PRODUCTION':
        kpis_stats = [
            {"kpi_name": "oee", "execution_time": 10.2, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/oee",
                         "num_call": "34"}},
            {"kpi_name": "av", "execution_time": 3, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/av",
                         "num_call": "11"}},
            {"kpi_name": "aq", "execution_time": 5.7, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/aq",
                         "num_call": "12"}},
            {"kpi_name": "pe", "execution_time": 2.7, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/pe",
                         "num_call": "5"}},
            {"kpi_name": "production_volume", "execution_time": 2.7, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/production_volume", "num_call": "12"}},
            {"kpi_name": "energy_consumption", "execution_time": 4.7, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/energy_consumption", "num_call": "12"}},
            {"kpi_name": "downtime_rate", "execution_time": 14.7, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/downtime_rate", "num_call": "12"}}
        ]
    elif taxonomy.upper() == 'BIOMEDICAL':
        kpis_stats = [
            {"kpi_name": "asimmetry_index", "execution_time": 10.7, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/asimmetry_index",
                         "num_call": "3"}},
            {"kpi_name": "difference_index", "execution_time": 45.2, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/difference_index", "num_call": "23"}}
        ]
    else:
        raise Exception("Taxonomy not found")

    return kpis_stats


@app.route('/kpi/<kpi_name>/<taxonomy>/stats', methods=['GET'])
@app.route('/kpi/<kpi_name>/stats', methods=['GET'])
def get_statistics(kpi_name=None, taxonomy=None):
    kpis_stats = get_kpi_stats(taxonomy)
    if (kpi_name is None or kpi_name.upper() == 'ALL') and ():
        # all kpis
        return jsonify(kpis_stats)
    else:
        # Cerca il KPI corrispondente nel dizionario
        kpi = next((item for item in kpis_stats if item["kpi_name"].upper() == kpi_name.upper()), None)
        return jsonify(kpi)


@app.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        connection = create_server_connection()
        query = "SELECT * FROM KPI_CATALOGUE ORDER BY last_update DESC LIMIT 1"
        result = read_query(connection, query)
        return jsonify("Executed" + result)
    except Exception as e:
        return jsonify({"error": f"An error occurred retrieving the KPIs. Error:{e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
