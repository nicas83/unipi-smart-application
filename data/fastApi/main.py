from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
from mysql.connector import errorcode
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from json import JSONEncoder
from typing import List

# To mange data field when returning the json to the caller
class DateEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

# db configs
db_config = {
    "user": "root",
    "password": "smartapp",
    "host": "127.0.0.1",
    "port": 3306,
    "database": "STORAGE",
}

# Connect to db
try:
    connection = mysql.connector.connect(**db_config)
    print("Connessione al database riuscita")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Errore: Accesso negato.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Errore: Database non esistente.")
    else:
        print(f"Errore: {err}")


class KPI(BaseModel):
    nome: str
    valore: float
    #data: date
    data: Optional[date] = None

class ApiResponse(BaseModel):
    message: str

app = FastAPI()


# Endpoint per aggiungere un kpi
# senza data: curl -X POST "http://localhost:8005/add_kpi" -H "accept: application/json" -H "Content-Type: application/json" -d '{"nome": "Kpi_8", "valore": 55}'
# con data: curl -X POST "http://localhost:8005/add_kpi" -H "accept: application/json" -H "Content-Type: application/json" -d '{"nome": "Kpi_9", "valore": 155, "data": "2023-11-10"}
@app.post("/add_kpi", response_model=KPI)
async def add_kpi(kpi: KPI):
    try:
        # Usa la data fornita nel corpo della richiesta, se presente, altrimenti utilizza la data corrente
        data = kpi.data or date.today()
        cursor = connection.cursor()
        query = f"INSERT INTO KPIS (NOME, VALORE, DATA) VALUES ('{kpi.nome}', {kpi.valore}, '{data}');"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        return kpi
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Errore del database: {err}")

# Endpoint
@app.get("/", response_model=ApiResponse)
async def api_center():
    return {"message": "KPI DATABASE"}

# Endpoint per ottenere tutti i KPI con data
# curl http://localhost:8005/allkpis 
@app.get("/allkpis", response_model=List[KPI])
async def get_kpis():
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM KPIS;"
        cursor.execute(query)
        kpis = cursor.fetchall()
        cursor.close()

        result = [
            KPI(nome=kpi["NOME"], valore=kpi["VALORE"], data=kpi["DATA"])
            for kpi in kpis
        ]
        return result

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Errore del database: {err}")


# Endpoint per ottenere un KPI specifico con data
#curl -X GET "http://localhost:8005/kpi?kpi_name=Kpi_1" -H "accept: application/json"
@app.get("/kpi", response_model=KPI)
async def get_kpi_by_name(kpi_name: str, include_date: Optional[bool] = False):
    try:
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM KPIS WHERE NOME = '{kpi_name}';"
        cursor.execute(query)
        kpi = cursor.fetchone()
        cursor.close()

        if not kpi:
            raise HTTPException(status_code=404, detail=f"KPI con nome {kpi_name} non trovato.")

        else:
            return KPI(nome=kpi["NOME"], valore=kpi["VALORE"], data=kpi["DATA"])
            
            

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Errore del database: {err}")
