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
N = 1

# Iterar sobre las filas del dataframe
primera_salida_mechanical = False
primera_salida_ebike = False
balance_mechanical = 0
balance_ebike = 0
balance_minimo_mechanical = 100 # Número grande arbitrario
balance_minimo_ebike = 100 # Número grande arbitrario
new_hour = True
first_mechanical = 0 # Valor inicial de bicicletas mecánicas a cada hora
first_ebike = 0 # Valor inicial de bicicletas eléctricas a cada hora
for index, row in df_bikes.iterrows():
    current_mechanical = row['num_bikes_available_types.mechanical']
    current_ebike = row['num_bikes_available_types.ebike']

    # Guardar primeras cantidades si es la primera fila de la hora
    if new_hour:
        first_mechanical = current_mechanical
        first_ebike = current_ebike
        balance_mechanical = first_mechanical
        balance_ebike = first_ebike
        diferencia_acumulada_mechanical = 0
        diferencia_acumulada_ebike = 0
        new_hour = False
    
    # Acumular salidas y entradas
    diff_mechanical = current_mechanical - previous_mechanical
    diff_ebike = current_ebike - previous_ebike
    diferencia_acumulada_mechanical = diff_mechanical
    diferencia_acumulada_ebike = diff_ebike
    balance_mechanical += diff_mechanical
    balance_ebike += diff_ebike

    if diff_mechanical < 0:
        if not primera_salida_mechanical:
            primera_salida_mechanical = True
        salidas_mecanicas += abs(diff_mechanical)
        # Al haber habido salida, vemos si se ha alcanzado un mínimo
        if (primera_salida_mechanical and balance_mechanical < balance_minimo_mechanical):
            balance_minimo_mechanical = balance_mechanical
    else:
        entradas_mecanicas += diff_mechanical

    if diff_ebike < 0:
        if not primera_salida_ebike:
            primera_salida_ebike = True
        salidas_electricas += abs(diff_ebike)
        # Al haber habido salida, vemos si se ha alcanzado un mínimo
        if (primera_salida_ebike and balance_ebike < balance_minimo_ebike):
            balance_minimo_ebike = balance_ebike
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

        if not primera_salida_mechanical:
            balance_minimo_mechanical = 0
        if not primera_salida_ebike:
            balance_minimo_ebike = 0

        total_salidas = salidas_mecanicas + salidas_electricas
        total_entradas = entradas_mecanicas + entradas_electricas
        demanda_mecanicas = salidas_mecanicas - entradas_mecanicas
        demanda_electricas = salidas_electricas - entradas_electricas
        total_demanda = total_salidas - total_entradas
        if diferencia_acumulada_mechanical != 0:
            min_required_mechanical = first_mechanical - balance_minimo_mechanical
        else:
            min_required_mechanical = 0
        if diferencia_acumulada_ebike != 0:
            min_required_ebike = first_ebike - balance_minimo_ebike
        else:
            min_required_ebike = 0
        
        hourly_data.append([total_salidas, salidas_mecanicas, salidas_electricas, 
                            entradas_mecanicas, entradas_electricas, total_entradas, 
                            demanda_mecanicas, demanda_electricas, total_demanda, 
                            previous_hour, row['day_week'], row['day_month'], 
                            row['month'], satisfy_demand, min_required_mechanical, min_required_ebike])
        
        # Reinicio de variables para la nueva hora
        new_hour = True
        first_mechanical = 0 # Valor inicial de bicicletas mecánicas a cada hora
        first_ebike = 0 # Valor inicial de bicicletas eléctricas a cada hora
        primera_salida_mechanical = False
        primera_salida_ebike = False
        balance_mechanical = 0
        balance_ebike = 0
        balance_minimo_mechanical = 100 # Número grande arbitrario
        balance_minimo_ebike = 100 # Número grande arbitrario

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
           'hour', 'day_week', 'day_month', 'month', 'satisfy_demand', 'min_required_mechanical', 'min_required_ebike']
df_hourly = pd.DataFrame(hourly_data, columns=columns)

# Escribir el DataFrame resultante en un nuevo archivo llamado DataFramePerHour.csv
df_hourly.to_csv('DataFramePerHour.csv', index=False)