import pandas as pd

# Cargar ambos archivos CSV
df_hourly = pd.read_csv('DataFramePerHour.csv')
df_meteo = pd.read_csv('Meteo_DataSet.csv')

# Realizar el 'merge' de los dos dataframes usando las columnas 'month', 'day_month' y 'hour'
merged_df = pd.merge(df_hourly, df_meteo[['month', 'day_month', 'hour', 'temperature', 'rain', 'windspeed']], 
                     on=['month', 'day_month', 'hour'], 
                     how='left')

# Guardar el DataFrame combinado de nuevo en 'DataFramePerHour.csv'
merged_df.to_csv('DataFramePerHourAndMeteo.csv', index=False)