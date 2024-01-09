import pandas as pd
from datetime import datetime, timedelta

# Cargar el dataset original
data_path = 'dataset_generation/temporary_datasets/OpenData_422_filtered.csv'  # Asegúrate de que la ruta sea correcta.
df = pd.read_csv(data_path)

# Convertir las columnas de fecha y hora en un único objeto datetime
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])

# Filtrar las fechas fuera del rango 1 de enero de 2021 a 30 de noviembre de 2023
start_date = datetime(2021, 1, 1, 0, 0)
end_date = datetime(2023, 11, 30, 23, 59)
df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]

# Función para determinar si la demanda fue satisfecha y obtener las bicicletas iniciales
def process_group(group):
    demand_satisfied = False if (group['num_bikes_available_types.ebike'] == 0).any() else True
    initial_bikes = group['num_bikes_available_types.ebike'].iloc[0]
    return pd.Series([demand_satisfied, initial_bikes], index=['demand_satisfied', 'initial_bikes'])

# Agrupar por año, mes, día y hora y aplicar la función
grouped_data = df.groupby(['year', 'month', 'day', 'hour']).apply(process_group).reset_index()

# Crear un rango completo de fechas y horas para asegurar que todas las horas estén presentes
full_range = pd.date_range(start=start_date, end=end_date, freq='H')
full_range_df = pd.DataFrame(full_range, columns=['datetime'])
full_range_df['year'] = full_range_df['datetime'].dt.year
full_range_df['month'] = full_range_df['datetime'].dt.month
full_range_df['day'] = full_range_df['datetime'].dt.day
full_range_df['hour'] = full_range_df['datetime'].dt.hour

# Unir con el rango completo para asegurarse de que todas las horas estén presentes
final_dataset = full_range_df.merge(grouped_data, on=['year', 'month', 'day', 'hour'], how='left')
final_dataset['demand_satisfied'].fillna('N/A', inplace=True)
final_dataset['initial_bikes'].fillna(0, inplace=True)  # Asumimos 0 si no hay datos

# Eliminar la columna 'datetime' del DataFrame final
final_dataset.drop('datetime', axis=1, inplace=True)

# Guardar el dataset final
final_dataset.to_csv('dataset_generation/temporary_datasets/demand_satisfied.csv', index=False)

print("Dataset generado y guardado correctamente.")
