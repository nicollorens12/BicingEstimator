import pandas as pd
import os
from datetime import datetime

# Directorios para cada año.
directories = {
    2021: 'dataset_generation/original_datasets/OpenDataBCN/2021',
    2022: 'dataset_generation/original_datasets/OpenDataBCN/2022',
    2023: 'dataset_generation/original_datasets/OpenDataBCN/2023'
}

# Función para procesar cada archivo.
def process_file(file_path):
    # Leer el dataset.
    df = pd.read_csv(file_path)

    # Filtrar por la estación 422.
    df = df[df['station_id'] == 422]

    # Convertir 'last_reported' de timestamp a datetime y extraer componentes temporales.
    df['datetime'] = pd.to_datetime(df['last_reported'], unit='s')
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute

    # Mantener solo las columnas temporales y el número de bicicletas eléctricas disponibles.
    df = df[['year', 'month', 'day', 'hour', 'minute', 'num_bikes_available_types.ebike']]

    return df

# Lista para guardar los datos de todos los archivos.
all_data = []

# Procesar cada archivo en cada directorio.
for year, directory in directories.items():
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                all_data.append(process_file(file_path))

# Concatenar todos los datos.
final_dataset = pd.concat(all_data)

# Ordenar cronológicamente.
final_dataset.sort_values(by=['year', 'month', 'day', 'hour', 'minute'], inplace=True)

# Guardar el dataset final.
final_dataset.to_csv('dataset_generation/temporary_datasets/OpenData_422_filtered.csv', index=False)

print("Dataset generado y guardado correctamente.")
