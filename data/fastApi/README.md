# FastAPI KPI Service

## Overview

This FastAPI service allows you to manage Key Performance Indicators (KPIs) with optional date information.

## Prerequisites
## app.py exposes a fast api webapp to interact with mysql db
NB: BEFORE EXECUTING THIS APP -> START THE MYSQL SERVICE AND READ THE README.md FILE located in ./mysql

1) CREATE A VIRTUAL ENVIRONMENT(NOT MANDATORY)  

    python3 -m venv venv
    source venv/bin/activate

2) INSTAL THE DEPENDENCIES

    pip3 install -r requirements.txt

3) RUN THE APPLICATION

    sudo uvicorn main:app --host localhost --port 8005 --reload

## Endpoints
1. Add a KPI
-   Request
    -   Method: POST
    -   URL: http://localhost:8005/add_kpi
    -   Headers:
        -   accept: application/json
        -   Content-Type: application/json
    -   Body, EAXAMPLE:
        -   Without date: 
                curl -X POST "http://localhost:8005/add_kpi" -H "accept: application/json" -H "Content-Type: application/json" -d '{"nome": "Kpi_8", "valore": 55}'
        -   With date:
                curl -X POST "http://localhost:8005/add_kpi" -H "accept: application/json" -H "Content-Type: application/json" -d '{"nome": "Kpi_9", "valore": 155,"data": "2023-11-10"}'
-   Response
    -   Body: JSON representation of the added KPI.

2. API Center
Request
Method: GET
URL: http://localhost:8005/
Response
Body: JSON with a message indicating the API center.

3. Get All KPIs
Request
Method: GET
URL: http://localhost:8005/allkpis
Response
Body: JSON array representing all KPIs with their names, values, and dates.
EXAMPLE: curl http://localhost:8005/allkpis

4. Get KPI by Name
Request
Method: GET
URL: http://localhost:8005/kpi?kpi_name=Kpi_1
Headers:
accept: application/json
Response
Body: JSON representation of the specified KPI with name, value, and date if available.
curl -X GET "http://localhost:8005/kpi?kpi_name=Kpi_1" -H "accept: application/json"





