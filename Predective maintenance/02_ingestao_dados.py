import pandas as pd
from sqlalchemy import create_engine

print("1. Lendo o arquivo CSV...")

caminho_do_csv = r"ai4i2020.csv"
df = pd.read_csv(caminho_do_csv)

df.columns = [
    'UDI', 'Product_ID', 'Type', 'Air_temperature_K', 'Process_temperature_K', 
    'Rotational_speed_rpm', 'Torque_Nm', 'Tool_wear_min', 'Machine_failure', 
    'TWF', 'HDF', 'PWF', 'OSF', 'RNF'
]

print("2. Conectando ao MySQL...")
engine = create_engine('mysql+pymysql://root:root@localhost:3306/manutencao_preditiva')

print("3. Injetando dados no banco (isso pode levar alguns segundos)...")
df.to_sql(name='telemetria_sensores', con=engine, if_exists='append', index=False)

print("Ingestão concluída com sucesso! Banco populado.")