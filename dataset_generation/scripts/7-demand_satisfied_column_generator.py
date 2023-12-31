import pandas as pd
import os
from datetime import datetime

# Función para procesar cada archivo.
def process_file(file_path):
    try:
        # Intentar leer el dataset con la codificación predeterminada (UTF-8).
        df = pd.read_csv(file_path)
    except UnicodeDecodeError:
        # Si hay un error de codificación, intentar con 'ISO-8859-1'.
        print(f"Error de codificación detectado en {file_path}. Intentando con ISO-8859-1...")
        df = pd.read_csv(file_path, encoding='ISO-8859-1')

    # Filtrar por la estación 422.
    df = df[df['station_id'] == 422]

    # Convertir timestamp a datetime.
    df['last_updated'] = pd.to_datetime(df['last_reported'], unit='s')

    # Extraer año, mes, día y hora.
    df['year'] = df['last_updated'].dt.year
    df['month'] = df['last_updated'].dt.month
    df['day'] = df['last_updated'].dt.day
    df['hour'] = df['last_updated'].dt.hour

    # Agrupar por año, mes, día y hora y verificar si la demanda fue satisfecha.
    demand_satisfied = df.groupby(['year', 'month', 'day', 'hour']).apply(
        lambda x: 'no data' if x.empty else (x['num_bikes_available_types.ebike'] > 0).all()
    ).reset_index(name='demand_satisfied')

    return demand_satisfied

# Crear un rango completo de fechas y horas.
start = datetime(2021, 1, 1)
end = datetime(2023, 11, 30, 23)  # Incluye hasta la última hora del 30 de noviembre de 2023.
full_range = pd.date_range(start, end, freq='H')
full_range_df = pd.DataFrame(full_range, columns=['datetime'])
full_range_df['year'] = full_range_df['datetime'].dt.year
full_range_df['month'] = full_range_df['datetime'].dt.month
full_range_df['day'] = full_range_df['datetime'].dt.day
full_range_df['hour'] = full_range_df['datetime'].dt.hour

# Directorios para cada año.
directories = {
    2021: 'dataset_generation/original_datasets/OpenDataBCN/2021',
    2022: 'dataset_generation/original_datasets/OpenDataBCN/2022',
    2023: 'dataset_generation/original_datasets/OpenDataBCN/2023'
}

# Lista para guardar los datos de todos los archivos.
all_data = []

# Procesar cada archivo en cada directorio.
for year, directory in directories.items():
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                try:
                    all_data.append(process_file(file_path))
                except Exception as e:
                    print(f"Error al procesar {file_path}: {e}")

# Concatenar todos los datos.
final_dataset = pd.concat(all_data)

# Unir con el rango completo para asegurarse de que todas las horas estén presentes.
final_dataset = full_range_df.merge(final_dataset, on=['year', 'month', 'day', 'hour'], how='left')
final_dataset['demand_satisfied'].fillna('N/A', inplace=True)

# Eliminar la columna 'datetime' del DataFrame final.
final_dataset.drop('datetime', axis=1, inplace=True)

# Guardar el dataset final.
final_dataset.to_csv('dataset_generation/temporary_datasets/demand_satisfaction.csv', index=False)

print("Dataset de la columna de demanda satisfecha generado correctamente.")
