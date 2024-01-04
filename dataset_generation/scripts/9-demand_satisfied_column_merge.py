import pandas as pd

# Cargar los conjuntos de datos originales
bicing_data = pd.read_csv('dataset_generation/temporary_datasets/dataset_without_demand_satisfied.csv')
demand_data = pd.read_csv('dataset_generation/temporary_datasets/demand_satisfied.csv')

bicing_data.drop_duplicates()

# Encontrar duplicados basados en las columnas de fecha y hora
duplicates = demand_data[demand_data.duplicated(subset=['year', 'month', 'day', 'hour'], keep=False)]

# Mostrar los duplicados si existen
if not duplicates.empty:
    print("Se encontraron los siguientes registros duplicados:")
    print(duplicates)
else:
    print("No se encontraron registros duplicados.")

# Eliminar duplicados, manteniendo la primera ocurrencia
demand_data = demand_data.drop_duplicates(subset=['year', 'month', 'day', 'hour'], keep='first')

# Ver que coincidan
print(bicing_data[['year', 'month', 'day', 'hour']].count())
print(demand_data[['year', 'month', 'day', 'hour']].count())

# Fusionar los conjuntos de datos utilizando las columnas de fecha y hora como clave
merged_data = pd.merge(bicing_data, demand_data, on=['year', 'month', 'day', 'hour'], how='outer', indicator=True)

# Separar los registros que no hacen match en ambos conjuntos de datos
no_match = merged_data[merged_data['_merge'] != 'both']

# Filtrar los registros que hacen match para el dataset final
final_data = merged_data[merged_data['_merge'] == 'both'].drop(columns=['_merge'])

# Reordenar las columnas del dataset final
final_data = final_data[['hour', 'day', 'month', 'year', 'week_day', 'exits', 'arrivals', 'temperature_2m', 'apparent_temperature', 'precipitation', 'rain', 'wind_speed_10m', 'demand_satisfied']]

# Guardar el nuevo conjunto de datos fusionado en un archivo CSV
final_data.to_csv('dataset_generation//dataset.csv', index=False)

# Opcional: Guardar los registros que no hacen match en otro archivo CSV para su revisión
no_match.to_csv('dataset_generation/temporary_datasets/raros.csv', index=False)

print("Proceso completado. El nuevo archivo CSV con datos fusionados ha sido creado.")
print(f"Se encontraron {len(no_match)} registros que no hacen match.")
