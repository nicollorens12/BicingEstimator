import os
import pandas as pd

# ATENCION! Este script tiene en cuenta que todos los .csv originales estan en la misma carpeta del script!!
current_directory = os.path.dirname(os.path.abspath(__file__))

# Listar todos los archivos CSV en el directorio actual
csv_files = [file for file in os.listdir(current_directory) if file.endswith(".csv")]

# Iterar a través de cada archivo CSV
for csv_file in csv_files:
    # Leer el archivo CSV
    df = pd.read_csv(os.path.join(current_directory, csv_file))
    
    # Filtrar las filas con 'station_id' igual a 422
    df_filtered = df[df['station_id'] == 422]
    
    # Construir el nombre del archivo de salida
    output_file = f"filtered_stations_{csv_file}"
    
    # Guardar el DataFrame filtrado como un nuevo archivo CSV en el directorio actual
    df_filtered.to_csv(os.path.join(current_directory, output_file), index=False)

print("Archivos CSV filtrados y guardados con éxito en el directorio actual.")
