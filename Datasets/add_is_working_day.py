import pandas as pd

# Cargar ambos archivos CSV
df_hourly = pd.read_csv('DataFramePerHour.csv')
df_holidays = pd.read_csv('dies_no_lectius.csv')

# Función para determinar si es un día laborable
def is_working_day(row):
    # Si es sábado o domingo, no es un día laborable
    if row['day_week'] > 5:
        return 0
    # Si es un día festivo (presente en df_holidays), no es un día laborable
    elif df_holidays[(df_holidays['day_month'] == row['day_month']) & (df_holidays['month'] == row['month'])].shape[0] > 0:
        return 0
    # En otros casos, es un día laborable
    return 1

# Aplicar la función a cada fila del DataFrame df_hourly
df_hourly['working_day'] = df_hourly.apply(is_working_day, axis=1)

# Guardar el DataFrame modificado de nuevo en 'DataFramePerHour.csv'
df_hourly.to_csv('DataFramePerHour.csv', index=False)