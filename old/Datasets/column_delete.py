import os
import pandas as pd

# Directorio actual donde se encuentra el script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Listar todos los archivos CSV que comienzan con "filtered_stations" en el directorio actual
csv_files = [file for file in os.listdir(current_directory) if file.startswith("filtered_stations") and file.endswith(".csv")]

# Columnas que deseas eliminar
columns_to_remove = ["station_id", "is_charging_station", "status", "is_installed", "is_renting", "is_returning", "traffic", "last_updated", "ttl"]

# Iterar a través de cada archivo CSV
for csv_file in csv_files:
    # Leer el archivo CSV
    df = pd.read_csv(os.path.join(current_directory, csv_file))
    
    # Eliminar las columnas especificadas
    df.drop(columns=columns_to_remove, inplace=True)
    
    # Guardar el DataFrame modificado en el mismo archivo CSV
    df.to_csv(os.path.join(current_directory, csv_file), index=False)

print("Columnas eliminadas de los archivos CSV con éxito en el directorio actual.")
