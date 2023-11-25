import json

import schedule
import time
import requests


from engine.core import KPICoreEngine


def retrieve_kpi_schedule(kpi_name="all"):
    url = f"http://example.com/get_kpi/" + kpi_name
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data


def job(frequency, kpi_name):
    # Creazione dell'istanza della tua classe
    if kpi_name == 'OEE':
        kpi = KPICoreEngine.calculate_oee(frequency)

    # Modifica la query in base alla frequenza di calcolo
    kpi.calculate_oee(frequency)


kpis = retrieve_kpi_schedule("all")

if 'kpi_data' in kpis:
    for kpi in kpis['kpi_data']:
        frequency = kpi['frequency']
        kpi_name = kpi['name']

        # Assumiamo che ci sia una corrispondenza tra il nome del KPI e una funzione di calcolo
        # Ad esempio, se il KPI è "oee", ci sarà una funzione chiamata "calculate_oee"
        job_function = globals().get(f'calculate_{kpi_name}', KPICoreEngine.calculate_generic_kpi(kpi_name))

        # Schedula il lavoro in base alla frequenza
        if frequency == 'daily':
            schedule.every().day.do(job_function, kpi_name)
        elif frequency == 'weekly':
            schedule.every().week.do(job_function, kpi_name)
        elif frequency == 'monthly':
            schedule.every().month.do(job_function, kpi_name)
        # Aggiungi qui altri casi per diverse frequenze se necessario

# Loop per eseguire i lavori schedulati
while True:
    schedule.run_pending()
    time.sleep(1)
