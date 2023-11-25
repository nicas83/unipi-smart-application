import configparser
import json


def config_influx_parser(path):
    config = configparser.ConfigParser()

    # Legge il file di configurazione
    config.read(path)

    # Recupera i valori
    url = config.get('DEFAULT', 'url')  # Recupera l'URL
    token = config.get('DEFAULT', 'token')  # Recupera il token
    org = config.get('DEFAULT', 'org')  # Recupera l'organizzazione
    bucket = config.get('DEFAULT', 'bucket')  # Recupera il bucket

    # Restituisce i valori in formato JSON
    return json.dumps({
        "url": url,
        "token": token,
        "org": org,
        "bucket": bucket
    })


def config_mysql_parser(path):
    config = configparser.ConfigParser()

    # Legge il file di configurazione
    config.read(path)

    # Recupera i valori
    host = config.get('DEFAULT', 'host')  # Recupera l'URL
    username = config.get('DEFAULT', 'username')  # Recupera il token
    password = config.get('DEFAULT', 'password')  # Recupera l'organizzazione
    database = config.get('DEFAULT', 'database')  # Recupera il bucket

    # Restituisce i valori in formato JSON
    return json.dumps({
        "host": host,
        "username": username,
        "password": password,
        "database": database
    })


def get_sqlconnection_string(path):
    config = configparser.ConfigParser()

    # Legge il file di configurazione
    config.read(path)

    return config.get('DEFAULT', 'conn_str')  # Recupera l'URL
