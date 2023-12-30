import pandas as pd

# Cargar el conjunto de datos original
data = pd.read_csv('scripts/TOTAL_meteo.csv')

# Convertir la columna 'date' a formato datedate
data['date'] = pd.to_datetime(data['date'])

# Crear nuevas columnas 'year', 'month', 'day', 'hour'
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month
data['day'] = data['date'].dt.day
data['hour'] = data['date'].dt.hour

# Eliminar la columna 'date'
data = data.drop(columns=['date'])

data = data[(data['year'] != 2020) & ((data['year'] < 2023) | ((data['year'] == 2023) & (data['month'] <= 11)))]

# Guardar el nuevo conjunto de datos en un nuevo archivo CSV
data.to_csv('scripts/barcelona_meteo_info.csv', index=False)

print("Proceso completado. El nuevo archivo CSV ha sido creado.")
