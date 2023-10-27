import pandas as pd

# Cargar el archivo DataFrame.csv desde el mismo directorio
df_bikes = pd.read_csv('DataFrame.csv')

# Convertir la columna de 'last_reported' a formato datetime
df_bikes['last_reported'] = pd.to_datetime(df_bikes['last_reported'], unit='s')
df_bikes = df_bikes.sort_values(by='last_reported')

# Variables de control y acumulación
hourly_data = []
previous_mechanical = 0
previous_ebike = 0
previous_hour = df_bikes.iloc[0]['hour']
salidas_mecanicas = 0
salidas_electricas = 0
entradas_mecanicas = 0
entradas_electricas = 0
no_bikes_counter = 0  # Contador para determinar si se ha satisfecho la demanda
satisfy_demand = True

# Constante para determinar cada cuántos instantes de tiempo consecutivos consideramos que no se ha satisfecho la demanda
N = 5

# Iterar sobre las filas del dataframe
for index, row in df_bikes.iterrows():
    current_mechanical = row['num_bikes_available_types.mechanical']
    current_ebike = row['num_bikes_available_types.ebike']
    
    # Acumular salidas y entradas
    diff_mechanical = current_mechanical - previous_mechanical
    diff_ebike = current_ebike - previous_ebike
    if diff_mechanical < 0:
        salidas_mecanicas += abs(diff_mechanical)
    else:
        entradas_mecanicas += diff_mechanical
    if diff_ebike < 0:
        salidas_electricas += abs(diff_ebike)
    else:
        entradas_electricas += diff_ebike
    
    # Verificar si no hay bicicletas disponibles
    if row['num_bikes_available'] == 0:
        no_bikes_counter += 1
    else:
        no_bikes_counter = 0

    # Si durante N instantes consecutivos, no había bicicletas, consideramos que no se ha satisfecho la demanda
    if no_bikes_counter == N:
        satisfy_demand = False

    # Si cambia la hora, guardar los datos acumulados y resetear las variables
    if row['hour'] != previous_hour:
        total_salidas = salidas_mecanicas + salidas_electricas
        total_entradas = entradas_mecanicas + entradas_electricas
        demanda_mecanicas = salidas_mecanicas - entradas_mecanicas
        demanda_electricas = salidas_electricas - entradas_electricas
        total_demanda = total_salidas - total_entradas
        
        hourly_data.append([total_salidas, salidas_mecanicas, salidas_electricas, 
                            entradas_mecanicas, entradas_electricas, total_entradas, 
                            demanda_mecanicas, demanda_electricas, total_demanda, 
                            previous_hour, row['day_week'], row['day_month'], 
                            row['month'], satisfy_demand])
        
        # Reinicio de variables para la nueva hora
        salidas_mecanicas = 0
        salidas_electricas = 0
        entradas_mecanicas = 0
        entradas_electricas = 0
        no_bikes_counter = 0
        satisfy_demand = True
        previous_hour = row['hour']
    
    previous_mechanical = current_mechanical
    previous_ebike = current_ebike

# Convertir la lista acumulada a un DataFrame
columns = ['total_salidas', 'salidas_mecanicas', 'salidas_electricas', 
           'entradas_mecanicas', 'entradas_electricas', 'total_entradas', 
           'demanda_mecanicas', 'demanda_electricas', 'total_demanda', 
           'hour', 'day_week', 'day_month', 'month', 'satisfy_demand']
df_hourly = pd.DataFrame(hourly_data, columns=columns)

# Escribir el DataFrame resultante en un nuevo archivo llamado DataFramePerHour.csv
df_hourly.to_csv('DataFramePerHour.csv', index=False)