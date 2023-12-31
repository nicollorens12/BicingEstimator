import pandas as pd

# Cargar los conjuntos de datos originales
bicing_data = pd.read_csv('dataset_generation/temporary_datasets/Exits_and_Arrivals_per_hour_422.csv')
meteo_data = pd.read_csv('dataset_generation/temporary_datasets/meteo_data_proper_date_format.csv')

# Fusionar los conjuntos de datos utilizando las columnas de fecha y hora
merged_data = pd.merge(bicing_data, meteo_data, on=['year', 'month', 'day', 'hour'], how='left')

# Filtrar y eliminar las filas correspondientes a diciembre de 2023
merged_data = merged_data[~((merged_data['year'] == 2023) & (merged_data['month'] == 12))]

# Guardar el nuevo conjunto de datos fusionado en un archivo CSV
merged_data.to_csv('dataset_generation/temporary_datasets/dataset_without_demand_satisfied.csv', index=False)

print("Proceso completado. El nuevo archivo CSV Bicing_Hours_Meteo.csv ha sido creado.")
