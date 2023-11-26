import requests

from data.influx_connection import DBConnection
from data.mysql_connection import create_server_connection, read_query, execute_query
from utils.utils import config_influx_parser
import re, parsley
import math



# define the Core Engine for kpi metric
class KPICoreEngine:
    def __init__(self):
        self.config = config_influx_parser('config/influx.properties')

    # Overall Equipment effectiveness: identifies the percentage of manufacturing time that is truly productive.
    # OEE Formula ---> OEE = AV * PE * QA
    def calculate_oee(self):
        # connect to the database MySQL
        connection = create_server_connection()
        query = ("select AV, PE, QA from KPI_CATALOGUE where kpi_name in ('AV', 'PE', 'QA') and last_update = "
                 "DATE_ADD(day,-1,curdate())")
        result = read_query(connection, query)
        av, pe, qa = 0, 0, 0
        for row in result:
            av += row[0]
            pe += row[1]
            qa += row[2]

        oee = av * qa * pe
        self.__save_kpi('OEE', oee)

    # PE FORMULA --->  PE(performance) = (Ideal Cycle Time * Total Count) / Operating Time * 100
    def calculate_pe(self):
        # create the connection to influx
        db_connection = DBConnection(url=self.config["url"], token=self.config["token"], bucket=self.config["bucket"],
                                     org=self.config["org"])

        query = ""

        result = db_connection.read_data(query)
        cycle_time, total_count, operating_time = 0, 0, 0
        for table in result:
            for record in table.records:
                cycle_time = record.values['cycle_time']
                total_count = record.values['total_count']
                operating_time = record.values['operating_time']

        pe = cycle_time * total_count / operating_time * 100
        self.__save_kpi('PE', pe)

    # AV Formula ----> AV(availability) = (Operating Time/Planned Time) * 100
    def calculate_av(self):
        # create the connection to influx
        db_connection = DBConnection(url=self.config["url"], token=self.config["token"], bucket=self.config["bucket"],
                                     org=self.config["org"])

        query = ""
        result = db_connection.read_data(query)
        operating_time, planned_time = 0, 0
        for table in result:
            for record in table.records:
                operating_time = record.values['operating_time']
                planned_time = record.values['planned_time']

        av = operating_time / planned_time * 100
        self.__save_kpi('AV', av)

    # QA Formula ----> QA(quality) = (Good Count/Total Count) * 100
    def calculate_qa(self):
        # create the connection to influx
        db_connection = DBConnection(url=self.config["url"], token=self.config["token"], bucket=self.config["bucket"],
                                     org=self.config["org"])

        query = ""
        result = db_connection.read_data(query)
        good_count, total_count = 0, 0
        for table in result:
            for record in table.records:
                good_count = record.values['good_count']
                total_count = record.values['total_count']

        qa = good_count / total_count * 100
        self.__save_kpi('QA', qa)

    def calculate_production_volume(self):
        pass

    def calculate_machine_utilization(self):
        pass

    def calculate_energy_consumption(self):
        pass

    # DR Formula ----> DR(Downtime Rate) = Down Hours / (Downtime Hours + Operational Hours)
    def calculate_downtime_rate(self):
        # create the connection to influx
        db_connection = DBConnection(url=self.config["url"], token=self.config["token"], bucket=self.config["bucket"],
                                     org=self.config["org"])

        # Query Flux
        query = '''
        downtime = from(bucket: "''mybucket''")
                     |> range(start: -1d)  # Modifica l'intervallo di tempo come necessario
                     |> filter(fn: (r) => r._measurement == "downtime_hours")

        operational = from(bucket: "''mybucket''")
                         |> range(start: -1d)  # Modifica l'intervallo di tempo come necessario
                         |> filter(fn: (r) => r._measurement == "operational_hours")

        join(tables: {downtime: downtime, operational: operational}, on: ["_time", "_measurement"])
        '''
        result = db_connection.read_data(query)
        downtime, operational = 0, 0
        for table in result:
            for record in table.records:
                downtime += record.values['downtime_hours']
                operational += record.values['operational_hours']

        downtime_rate = downtime / (downtime + operational)
        self.__save_kpi('DR', downtime_rate)

    def calculate_generic_kpi(self, kpi_name):
        url = "http://localhost:8086/get_kpi/"+kpi_name
        response = requests.get(url + kpi_name)
        data = response.json()

        ############################# WIP - KPI Parser #############################
        
        def calculate(start, pairs):
            result = start
            for op, *values in pairs:
                value = extract_value(values[0])
                if op == '+':
                    if isinstance(result, (int, float)) and isinstance(value, (int, float)):
                        result += value
                    else:
                        result = str(result) + str(value)
                elif op == '-':
                    result -= value
                elif op == '*':
                    result *= value
                elif op == '/':
                    result /= value
                elif op == '^':
                    result **= value
                elif op == 'sqrt':
                    result = math.sqrt(value)
                elif op == 'min':
                    result = min(*map(extract_value, values))
                elif op == 'max':
                    result = max(*map(extract_value, values))
                elif op == 'avg':
                    result = sum(map(extract_value, values[0])) / len(values[0])
                elif op == 'count':
                    result += 1
            return result

        def extract_value(value):
            if isinstance(value, tuple):
                return extract_value(value[0])
            if isinstance(value, str) and value.isnumeric():
                return float(value)
            return value

        x = parsley.makeGrammar("""
        number = <digit+>:ds -> int(ds)
        parens = '(' ws expr:e ws ')' -> e
        value = number | parens | func_call
        ws = ' '*
        add = '+' ws expr2:n -> ('+', n)
        sub = '-' ws expr2:n -> ('-', n)
        mul = '*' ws value:n -> ('*', n)
        div = '/' ws value:n -> ('/', n)
        exp = '^' ws value:n -> ('^', n)
        func_call = sqrt_op | min_op | max_op | avg_op | count_op
        sqrt_op = 'sqrt(' ws expr2:n ws ')' -> ('sqrt', n)
        min_op = 'min(' ws expr2:n ws ',' ws expr2:n ws ')' -> ('min', n, n)
        max_op = 'max(' ws expr2:n ws ',' ws expr2:n ws ')' -> ('max', n, n)
        avg_op = 'avg(' ws expr2:n ws ',' ws expr2:n ws ')' -> ('avg', n, n)
        count_op = 'count()' ws -> ('count', None)

        addsub = ws (add | sub)
        muldiv = ws (mul | div | exp | func_call)

        expr = expr2:left addsub*:right -> calculate(left, right)
        expr2 = value:left muldiv*:right -> calculate(left, right)
        """, {"calculate": calculate})

        print(x("1 + (1+1)*(2-1) + 1 + (1/2) + 1*4 + 67").expr())

        ############################# WIP - KPI Parser #############################
        # TODO: logica di calcolo kpi generico
        value = 0 # da calcolare
        self.__save_kpi(kpi_name, value)

    @staticmethod
    def __save_kpi(kpi_name, value) -> None:
        # save kpi to mysql
        connection = create_server_connection()
        write_query = "insert into KPI (kpi_name, value, last_update) values ('" + kpi_name + "'," + value + ", now())"
        execute_query(connection, write_query)
