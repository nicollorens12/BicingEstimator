import pandas as pd
from datetime import datetime, timedelta

# Cargar el conjunto de datos original
data = pd.read_csv('dataset_generation/temporary_datasets/Exits_and_Arrivals_422.csv', delimiter=',')

# Convertir la columna 'time' a formato datetime
data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S,%f')

# Crear nuevas columnas con la información deseada
data['year'] = data['time'].dt.year
data['month'] = data['time'].dt.month
data['day'] = data['time'].dt.day
data['week_day'] = data['time'].dt.day_name()
data['hour'] = data['time'].dt.hour

# Crear columnas 'exits' y 'arrivals'
data['exits'] = (data['trip_type'] == 'Salida').astype(int)
data['arrivals'] = (data['trip_type'] == 'Llegada').astype(int)

# Generar un rango de fechas y horas
date_range = pd.date_range(start=data['time'].min(), end=data['time'].max(), freq='H')

# Crear un DataFrame con el rango de fechas y horas
hourly_data = pd.DataFrame({'time': date_range})
hourly_data['year'] = hourly_data['time'].dt.year
hourly_data['month'] = hourly_data['time'].dt.month
hourly_data['day'] = hourly_data['time'].dt.day
hourly_data['week_day'] = hourly_data['time'].dt.day_name()
hourly_data['hour'] = hourly_data['time'].dt.hour

# Combinar el DataFrame original con el DataFrame de horas
merged_data = pd.merge(hourly_data, data, on=['year', 'month', 'day', 'week_day', 'hour'], how='left')

# Llenar NaN con 0 en las columnas 'exits' y 'arrivals'
merged_data['exits'] = merged_data['exits'].fillna(0).astype(int)
merged_data['arrivals'] = merged_data['arrivals'].fillna(0).astype(int)

# Realizar una agregación para sumar los valores duplicados
final_data = merged_data.groupby(['year', 'month', 'day', 'week_day', 'hour'], as_index=False).agg({'exits': 'sum', 'arrivals': 'sum'})

# Guardar el nuevo conjunto de datos en un nuevo archivo CSV
final_data.to_csv('dataset_generation/temporary_datasets/Exits_and_Arrivals_per_hour_422.csv', index=False)

print("Proceso completado. El nuevo archivo CSV ha sido creado.")
