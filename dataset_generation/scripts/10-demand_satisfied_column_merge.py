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

# Renombrar columnas
final_data.rename(columns={
    'temperature_2m': 'temperature',
    'apparent_temperature': 'a_temperature',
    'relative_humidity_2m': 'humidity',
    'wind_speed_10m': 'wind_speed'
}, inplace=True)

# Convertir 'week_day' de nombre a número (0-6)
week_day_mapping = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
final_data['week_day'] = final_data['week_day'].map(week_day_mapping)

# Convertir 'demand_satisfied' a 1 para 'True', 0 para 'False', y dejar los missing values como NaN
final_data['demand_satisfied'] = final_data['demand_satisfied'].map({True: 1, False: 0})

# Redondear columnas con valores decimales a tres dígitos
cols_to_round = ['temperature', 'a_temperature', 'humidity', 'precipitation', 'rain', 'wind_speed']
final_data[cols_to_round] = final_data[cols_to_round].round(1)

# ACLARAR MISSING VALUES A NaN -----------------------------------------
# Definir los rangos de fechas para los cuales los valores deben establecerse como NaN
# Las fechas están en el formato 'año-mes-día'
august_start = '2023-08-22'
august_end = '2023-08-31'
september_start = '2023-09-01'
september_end = '2023-09-05'

# Convertir las columnas 'year', 'month', 'day' a un objeto datetime para comparación
final_data['date'] = pd.to_datetime(final_data[['year', 'month', 'day']])

# Establecer a NaN los valores de 'demand_satisfied' y 'initial_bikes' para los rangos de fechas especificados
final_data.loc[(final_data['date'] >= august_start) & (final_data['date'] <= august_end), ['demand_satisfied', 'initial_bikes']] = pd.NA
final_data.loc[(final_data['date'] >= september_start) & (final_data['date'] <= september_end), ['demand_satisfied', 'initial_bikes']] = pd.NA

# Eliminar la columna 'date' como se solicitó
final_data.drop('date', axis=1, inplace=True)

# Reordenar las columnas del dataset final
final_data = final_data[['hour', 'day', 'month', 'year', 'week_day', 'working_day', 'class_day', 'exits', 'temperature', 'a_temperature', 'humidity', 'precipitation', 'rain', 'wind_speed', 'demand_satisfied', 'initial_bikes']]

# Guardar el nuevo conjunto de datos fusionado en un archivo CSV
final_data.to_csv('dataset_generation//dataset.csv', index=False)

# Opcional: Guardar los registros que no hacen match en otro archivo CSV para su revisión
no_match.to_csv('dataset_generation/temporary_datasets/raros.csv', index=False)

print("Proceso completado. El nuevo archivo CSV con datos fusionados ha sido creado.")
print(f"Se encontraron {len(no_match)} registros que no hacen match.")
