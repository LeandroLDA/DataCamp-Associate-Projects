import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Ajuste para evitar erro de Winutils no Windows
os.environ["HADOOP_HOME"] = "C:\\hadoop"
os.environ["PATH"] += os.pathsep + "C:\\hadoop\\bin"

# 1. Iniciando o motor Spark
# Certifique-se de que o arquivo .jar está na pasta 'lib' do seu projeto
spark = SparkSession.builder \
    .appName("Manutencao_Preditiva_Silver") \
    .config("spark.jars", "lib/mysql-connector-j-9.6.0.jar") \
    .getOrCreate()
    
spark.sparkContext.setLogLevel("ERROR")

print("Motor Spark em funcionamento!")

# 2. Lendo a Camada Bronze (MySQL)
df_bronze = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/manutencao_preditiva") \
    .option("dbtable", "telemetria_sensores") \
    .option("user", "root") \
    .option("password", "root") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .load()

# 3. Transformação para Camada Silver (Refino Técnico)
window_spec = Window.orderBy("UDI").rowsBetween(-10, 0)

df_silver = df_bronze \
    .withColumn("Temp_Celsius", F.round(F.col("Process_temperature_K") - 273.15, 2)) \
    .withColumn("Media_Movel_Temp", F.round(F.avg("Temp_Celsius").over(window_spec), 2)) \
    .withColumn("Potencia_Watts", F.round(F.col("Torque_Nm") * (F.col("Rotational_speed_rpm") * 0.1047), 2)) \
    .withColumn("Status_Critico", F.when((F.col("Temp_Celsius") > 40) & (F.col("Potencia_Watts") > 5000), 1).otherwise(0))

# Teste de carga: Quantas linhas o Spark carregou?
total_linhas = df_silver.count()
print(f"Total de registros processados: {total_linhas}")

if total_linhas > 0:
    print("Amostra dos dados refinados (Camada Silver):")
    df_silver.select("Product_ID", "Temp_Celsius", "Media_Movel_Temp", "Potencia_Watts", "Status_Critico").show(10)
else:
    print("Atenção: Nenhuma linha encontrada. Verifique se a tabela no MySQL tem dados.")

# 4. Exibindo o resultado do seu trabalho de Engenharia
print("Dados Processados (Camada Silver):")
df_silver.select("Product_ID", "Temp_Celsius", "Media_Movel_Temp", "Potencia_Watts", "Status_Critico").show(10)

# Para fechar com chave de ouro: Salvar como Parquet (formato profissional)
# df_silver.write.mode("overwrite").parquet("camada_silver_telemetria.parquet")