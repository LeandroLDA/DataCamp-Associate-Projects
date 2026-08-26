CREATE DATABASE IF NOT EXISTS manutencao_preditiva;
USE manutencao_preditiva;

CREATE TABLE IF NOT EXISTS telemetria_sensores (
    UDI INT PRIMARY KEY,
    Product_ID VARCHAR(50),
    Type VARCHAR(10),
    Air_temperature_K FLOAT,
    Process_temperature_K FLOAT,
    Rotational_speed_rpm INT,
    Torque_Nm FLOAT,
    Tool_wear_min INT,
    Machine_failure INT,
    TWF INT,
    HDF INT,
    PWF INT,
    OSF INT,
    RNF INT
);

LOAD DATA INFILE '"C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\ai4i2020.csv'
INTO TABLE telemetria_sensores
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS; 