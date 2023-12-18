import pandas as pd

# Cargar el conjunto de datos original
data = pd.read_csv('barcelona_meteo_info.csv')

# Convertir la columna 'time' a formato datetime
data['time'] = pd.to_datetime(data['time'])

# Crear nuevas columnas 'year', 'month', 'day', 'hour'
data['year'] = data['time'].dt.year
data['month'] = data['time'].dt.month
data['day'] = data['time'].dt.day
data['hour'] = data['time'].dt.hour

# Eliminar la columna 'time'
data = data.drop(columns=['time'])

# Guardar el nuevo conjunto de datos en un nuevo archivo CSV
data.to_csv('barcelona_meteo_info.csv', index=False)

print("Proceso completado. El nuevo archivo CSV ha sido creado.")
