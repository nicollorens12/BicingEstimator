import os
import pandas as pd
from datetime import datetime


# Directorio actual donde se encuentra el script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Listar todos los archivos CSV que comienzan con "filtered_stations" en el directorio actual
csv_files = [file for file in os.listdir(current_directory) if file.startswith("filtered_stations") and file.endswith(".csv")]

# Inicializar un DataFrame vacío para contener todos los datos
final_df = pd.DataFrame()

# Iterar a través de cada archivo CSV y combinarlos en un solo DataFrame
for csv_file in csv_files:
    df = pd.read_csv(os.path.join(current_directory, csv_file))
    final_df = pd.concat([final_df, df], ignore_index=True)

# Agregar columnas para el mes, el día del mes, la hora y los minutos
final_df["month"] = final_df["last_reported"].apply(lambda x: datetime.utcfromtimestamp(x).month)
final_df["day_month"] = final_df["last_reported"].apply(lambda x: datetime.utcfromtimestamp(x).day)
final_df["day_week"] = final_df["last_reported"].apply(lambda x: datetime.utcfromtimestamp(x).weekday())
final_df["hour"] = final_df["last_reported"].apply(lambda x: datetime.utcfromtimestamp(x).hour)
final_df["minute"] = final_df["last_reported"].apply(lambda x: datetime.utcfromtimestamp(x).minute)

# Encara no esborrem last_reported perquè ho utilitzem per ordenar cronològicament 
# final_df.drop(columns=['V1', 'last_reported'], inplace=True)
final_df.drop(columns=['V1'], inplace=True)

# Guardar el DataFrame combinado en un solo archivo CSV llamado "DataFrame.csv"
final_df.to_csv(os.path.join(current_directory, "DataFrame.csv"), index=False)

print("Archivos CSV combinados en 'DataFrame.csv' con columnas de tiempo y columna 'festivo' agregada con éxito en el directorio actual.")
