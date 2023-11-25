from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS


class DBConnection:
    def __init__(self, url, token, bucket, org):
        self.url = url
        self.token = token
        self.bucket = bucket
        self.org = org

    def __get_connection(self):
        return InfluxDBClient(url=self.url, token=self.token, org=self.org)

    def get_bucket(self):
        return self.bucket

    def get_org(self):
        return self.org

    def read_data(self, query):
        client = self.__get_connection()
        result = client.query_api().query(org=self.get_org(), query=query)
        client.close()
        return result

    def write_data(self, data):
        client = self.__get_connection()
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=self.get_bucket(), org=self.get_org(), record=data)
        client.close()

