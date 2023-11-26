import requests
from flask import Flask, request, jsonify

from data.mysql_connection import create_server_connection, read_query

app = Flask(__name__)

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


@app.route('/kpi/<kpi_name>', methods=['GET'])
def get_kpi_by_name(kpi_name):
    try:
        print("getting connection")
        # connection = create_server_connection(conn_str)
        print("connection created")
        query = "SELECT * FROM KPI_CATALOGUE WHERE kpi_name = %s" + kpi_name.upper() + "ORDER BY last_update DESC LIMIT 1"
        # result = read_query(connection, query)

        kpis = None
        # creo il json da restituire al FE
        # kpis = [{"kpi_name": row[0], "value": row[1], "last_update": row[2]} for row in result]
        if kpi_name.upper() == 'OEE':
            kpis = [
                {"kpi_name": "OEE", "value": 10.2, "taxonomy": "PRODUCTION", "group_by": "ALL", "last_update": "2023-11-23T00:00:00.000Z"}]
        elif kpi_name.upper() == "AV":
            kpis = [
                {"kpi_name": "AV", "value": 4.5, "taxonomy": "PRODUCTION", "group_by": "ALL", "last_update": "2023-11-24T00:00:00.000Z"}]
        elif kpi_name.upper() == "AQ":
            kpis = [
                {"kpi_name": "AQ", "value": 11.7, "taxonomy": "PRODUCTION", "group_by": "ALL", "last_update": "2023-11-25T00:00:00.000Z"}]
        elif kpi_name.upper() == "PE":
            kpis = [
                {"kpi_name": "PE", "value": 3.7, "taxonomy": "PRODUCTION", "group_by": "ALL", "last_update": "2023-11-25T00:00:00.000Z"}]
        elif kpi_name.upper() == "AHA":
            kpis = [{"kpi_name": "AHA", "value": 0.7, "taxonomy": "BIOMEDICAL", "group_by": "PATIENT_1",
                     "last_update": "2023-11-25T00:00:00.000Z"}]
        elif kpi_name.upper() == "EH":
            kpis = [{"kpi_name": "EH", "value": 0.05, "taxonomy": "BIOMEDICAL", "group_by": "PATIENT_2",
                     "last_update": "2023-11-24T00:00:00.000Z"}]
        elif kpi_name.upper() == "DOWNTIME_RATE":
            kpis = [{"kpi_name": "DOWNTIME_RATE", "value": 0.7, "taxonomy": "PRODUCTION", "group_by": "ALL",
                     "last_update": "2023-11-25T00:00:00.000Z"}]
        elif kpi_name.upper() == "ENERGY_CONSUMPTION":
            kpis = [{"kpi_name": "ENERGY_CONSUMPTION", "value": 320.7, "taxonomy": "PRODUCTION", "group_by": "ALL",
                     "last_update": "2023-11-25T00:00:00.000Z"}]
        elif kpi_name.upper() == "PRODUCTION_VOLUME":
            kpis = [{"kpi_name": "PRODUCTION_VOLUME", "value": 200, "taxonomy": "PRODUCTION", "group_by": "ALL",
                     "last_update": "2023-11-25T00:00:00.000Z"}]
        return jsonify(kpis)
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
        kpis = [
            {"kpi_name": "OEE", "value": 10.2, "taxonomy": "", "group_by": "", "last_update": "2023-11-23T00:00:00.000Z"},
            {"kpi_name": "AV", "value": 5, "taxonomy": "", "group_by": "", "last_update": "2023-11-24T00:00:00.000Z"},
            {"kpi_name": "AQ", "value": 3.7, "taxonomy": "", "group_by": "", "last_update": "2023-11-25T00:00:00.000Z"},
            {"kpi_name": "PE", "value": 0.7, "taxonomy": "", "group_by": "", "last_update": "2023-11-25T00:00:00.000Z"},
            {"kpi_name": "PRODUCTION_VOLUME", "value": 200, "taxonomy": "", "group_by": "", "last_update": "2023-11-25T00:00:00.000Z"},
            {"kpi_name": "DOWNTIME_RATE", "value": 0.7, "taxonomy": "", "group_by": "", "last_update": "2023-11-25T00:00:00.000Z"},
            {"kpi_name": "ENERGY_CONSUMPTION", "value": 320.7, "taxonomy": "", "group_by": "", "last_update": "2023-11-25T00:00:00.000Z"},
            {"kpi_name": "AHA", "value": 10.7, "taxonomy": "", "group_by": "", "last_update": "2023-11-25T00:00:00.000Z"},
            {"kpi_name": "EH", "value": 10.7, "taxonomy": "", "group_by": "", "last_update": "2023-11-25T00:00:00.000Z"}
        ]

        return jsonify(kpis)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred retrieving the KPIs. Error:{e}"}), 500


@app.route('/kpi/<kpi_name>/stats', methods=['GET'])
def get_kpi_stats(kpi_name):
    kpis = None
    if kpi_name == '' or kpi_name.upper() == 'ALL':
        # all kpis
        kpis = [
            {"kpi_name": "OEE", "execution_time": 10.2, "last_update": "2023-11-23T00:00:00.000Z", "details": {"api_name": "/kpi/oee",
                                                                                          "num_call": "34"}},
            {"kpi_name": "AV", "execution_time": 3, "last_update": "2023-11-23T00:00:00.000Z", "details": {"api_name": "/kpi/av",
                                                                                      "num_call": "11"}},
            {"kpi_name": "AQ", "execution_time": 5.7, "last_update": "2023-11-23T00:00:00.000Z", "details": {"api_name": "/kpi/aq",
                                                                                        "num_call": "12"}},
            {"kpi_name": "PE", "execution_time": 2.7, "last_update": "2023-11-23T00:00:00.000Z", "details": {"api_name": "/kpi/pe",
                                                                                        "num_call": "5"}},
            {"kpi_name": "PRODUCTION_VOLUME", "execution_time": 2.7, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/production_volume", "num_call": "12"}},
            {"kpi_name": "ENERGY_CONSUMPTION", "execution_time": 4.7, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/energy_consumption", "num_call": "12"}},
            {"kpi_name": "DOWNTIME_RATE", "execution_time": 14.7, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/downtime_rate", "num_call": "12"}}
        ]
    elif kpi_name.upper() == 'OEE':
        # oee
        kpis = [
            {"kpi_name": "OEE", "execution_time": 10.2, "last_update": "2023-11-23T00:00:00.000Z", "details": {"api_name": "/kpi/aha",
                                                                                          "num_call": "12"}}]
    elif kpi_name.upper() == 'AV':
        # av
        kpis = [
            {"kpi_name": "AV", "execution_time": 5.4, "last_update": "2023-11-23T00:00:00.000Z", "details": {"api_name": "/kpi/aha",
                                                                                        "num_call": "11"}}]
    elif kpi_name.upper() == 'AQ':
        # aq
        kpis = [
            {"kpi_name": "AQ", "execution_time": 3.7, "last_update": "2023-11-23T00:00:00.000Z", "details": {"api_name": "/kpi/aha",
                                                                                        "num_call": "34"}}]
    elif kpi_name.upper() == 'PE':
        # pe
        kpis = [
            {"kpi_name": "PE", "execution_time": 7.3, "last_update": "2023-11-23T00:00:00.000Z", "details": {"api_name": "/kpi/aha",
                                                                                        "num_call": "124"}}]
    elif kpi_name.upper() == 'AHA':
        # aha
        kpis = [
            {"kpi_name": "AHA", "execution_time": 12.5, "last_update": "2023-11-23T00:00:00.000Z", "details": {"api_name": "/kpi/aha",
                                                                                          "num_call": "3"}}]
    elif kpi_name.upper() == 'EH':
        # eh
        kpis = [
            {"kpi_name": "EH", "execution_time": 45.2, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/aha", "num_call": "23"}}]
    elif kpi_name.upper() == 'DOWNTIME_RATE':
        # downtime rate
        kpis = [
            {"kpi_name": "DOWNTIME_RATE", "execution_time": 2.2, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/aha", "num_call": "41"}}]
    elif kpi_name.upper() == 'ENERGY_CONSUMPTION':
        # energy consumption
        kpis = [
            {"kpi_name": "ENERGY_CONSUMPTION", "execution_time": 8.2, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/aha", "num_call": "13"}}]
    elif kpi_name.upper() == 'PRODUCTION_VOLUME':
        # production volume
        kpis = [
            {"kpi_name": "PRODUCTION_VOLUME", "execution_time": 3.2, "last_update": "2023-11-23T00:00:00.000Z",
             "details": {"api_name": "/kpi/aha", "num_call": "34"}}]
    else:
        # error
        raise Exception

    return jsonify(kpis)


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
