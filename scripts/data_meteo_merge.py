import pandas as pd

# Cargar los conjuntos de datos originales
bicing_data = pd.read_csv('scripts/Bicing_Hours.csv')
meteo_data = pd.read_csv('scripts/barcelona_meteo_info.csv')

# Fusionar los conjuntos de datos utilizando las columnas de fecha y hora
merged_data = pd.merge(bicing_data, meteo_data, on=['year', 'month', 'day', 'hour'], how='left')

# Guardar el nuevo conjunto de datos fusionado en un archivo CSV
merged_data.to_csv('Bicing_Hours_Meteo.csv', index=False)

print("Proceso completado. El nuevo archivo CSV Bicing_Hours_Meteo.csv ha sido creado.")
