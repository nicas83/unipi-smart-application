# INFO
this directory contains a mysql db instance that will store the key-value pairs: <kpi_name, value> 

# RUN THE mysql IMAGE
sudo docker-compose up 

# !! N.B.:(first time only) CREATE THE DATABASE !!

new terminal, same directory:

-   sudo docker exec -it mysqldb1 mysql -u root -p
-   password: smartapp

create the database:

-   CREATE DATABASE STORAGE;

select it:

-   USE STORAGE; 

create a table:

-   CREATE TABLE KPIS (
    NOME VARCHAR(20),
    VALORE FLOAT,
    DATA DATE
    );

check if the table is created:

-   SHOW TABLES;

exit:

-   exit


# REQUIREMENTS
pip3 install -r requirements.txt

# APP EXECUTION
python3 app.py

# app.py
N.B.: if you have not created the databae or you have changed the configuration parameter/db name or db/table this will affect the whole execution of the script!
This script interacts with the mysql container.
Allows you (for now) to interact manually with the db (i.e. show the kpis, add, delete etc...)
The very first time the kpi-database STORAGE will be empty, after the creation.

Shell: insert 1 || 2 || 3 || 4

1: visualize the databases 
2: it expects a number(n); it generates n-kpis with an integer random value (1,100). the first time starts with id = 1 and progressively starts to increment the ids form the last kpi's id written in the table KPIS
3: shows the content of the db
4: eliminates all the records (all the kpis). It won't eliminate the table KPIS

# config.yaml
db configuration infos: es credentials
# data directiory
contains the volume of the mysqldb image (the proper database).
The first time will be empty.

# STOP THE EXECUTION 
- sudo docker-compose down