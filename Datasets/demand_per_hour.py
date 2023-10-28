import pandas as pd

# Cargar el archivo DataFrame.csv desde el mismo directorio
df_bikes = pd.read_csv('DataFrame.csv')

# Convertir la columna de 'last_reported' a formato datetime
df_bikes['last_reported'] = pd.to_datetime(df_bikes['last_reported'], unit='s')
df_bikes = df_bikes.sort_values(by='last_reported')

# Variables de control y acumulación
hourly_data = []
disponibilidad_mecanicas_anterior = 0
disponibilidad_electricas_anterior = 0
previous_hour = df_bikes.iloc[0]['hour']
salidas_mecanicas = 0
salidas_electricas = 0
entradas_mecanicas = 0
entradas_electricas = 0
no_bikes_counter = 0  # Contador para determinar si se ha satisfecho la demanda
satisfy_demand = True

# Constante para determinar cada cuántos instantes de tiempo consecutivos consideramos que no se ha satisfecho la demanda
N = 1


# --------------------------------------------------------------------------------------------------
# BUCLE QUE ITERA LAS FILAS DEL DATAFRAME ##########################################################
# --------------------------------------------------------------------------------------------------

# -----> INICIALIZACION DE VARIABLES PREVIA AL BUCLE
primera_salida_mechanical = False
primera_salida_ebike = False
balance_mechanical = 0
balance_ebike = 0
disponibilidad_minima_mecanicas_tras_primera_salida = 100 # Número grande arbitrario
disponibilidad_minima_electricas_tras_primera_salida = 100 # Número grande arbitrario
hora_nueva = True
disponibilidad_mecanicas_inicial = 0 # Valor inicial de bicicletas mecánicas a cada hora
disponibilidad_electricas_inicial = 0 # Valor inicial de bicicletas eléctricas a cada hora

# -----> INICIO DEL BUCLE
for index, row in df_bikes.iterrows():
    disponibilidad_mecanicas_actual = row['num_bikes_available_types.mechanical']
    disponibilidad_electricas_actual = row['num_bikes_available_types.ebike']

    # Guardar primeras cantidades si es la primera fila de la hora
    if hora_nueva:
        disponibilidad_mecanicas_inicial = disponibilidad_mecanicas_actual
        disponibilidad_electricas_inicial = disponibilidad_electricas_actual
        balance_mechanical = disponibilidad_mecanicas_inicial
        balance_ebike = disponibilidad_electricas_inicial
        diferencia_acumulada_mechanical = 0
        diferencia_acumulada_ebike = 0
        hora_nueva = False
    
    # Calcular diferencias por cada cambio de fila
    diferencia_mecanicas = disponibilidad_mecanicas_actual - disponibilidad_mecanicas_anterior
    diferencia_electricas = disponibilidad_electricas_actual - disponibilidad_electricas_anterior
    diferencia_acumulada_mechanical += diferencia_mecanicas
    diferencia_acumulada_ebike += diferencia_electricas
    # balance_mechanical += diferencia_mecanicas
    # balance_ebike += diferencia_electricas

    # Si se han producido salidas de mecanicas...
    if diferencia_mecanicas < 0:
        if not primera_salida_mechanical:
            primera_salida_mechanical = True
        salidas_mecanicas += abs(diferencia_mecanicas)
        # Al haber habido salida, vemos si se ha alcanzado un mínimo
        if (primera_salida_mechanical and disponibilidad_mecanicas_actual < disponibilidad_minima_mecanicas_tras_primera_salida):
            disponibilidad_minima_mecanicas_tras_primera_salida = disponibilidad_mecanicas_actual
    # Sino si se han producido entradas de mecanicas...
    else:
        entradas_mecanicas += diferencia_mecanicas

    # Si se han producido salidas de electricas...
    if diferencia_electricas < 0:
        if not primera_salida_ebike:
            primera_salida_ebike = True
        salidas_electricas += abs(diferencia_electricas)
        # Al haber habido salida, vemos si se ha alcanzado un mínimo
        if (primera_salida_ebike and disponibilidad_electricas_actual < disponibilidad_minima_electricas_tras_primera_salida):
            disponibilidad_minima_electricas_tras_primera_salida = disponibilidad_electricas_actual
    # Sino si se han producido entradas de electricas...
    else:
        entradas_electricas += diferencia_electricas
    
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
            disponibilidad_minima_mecanicas_tras_primera_salida = 0
        if not primera_salida_ebike:
            disponibilidad_minima_electricas_tras_primera_salida = 0

        total_salidas = salidas_mecanicas + salidas_electricas
        total_entradas = entradas_mecanicas + entradas_electricas

        if diferencia_acumulada_mechanical != 0:
            min_required_mechanical = disponibilidad_mecanicas_inicial - disponibilidad_minima_mecanicas_tras_primera_salida
            # Si es negativo, decimos que es 0, ya que en principio no consideraremos excedentes
            if min_required_mechanical < 0:
                min_required_mechanical = 0
        else:
            min_required_mechanical = 0
        if diferencia_acumulada_ebike != 0:
            min_required_ebike = disponibilidad_electricas_inicial - disponibilidad_minima_electricas_tras_primera_salida
            # Si es negativo, decimos que es 0, ya que en principio no consideraremos excedentes
            if min_required_ebike < 0:
                min_required_ebike = 0
        else:
            min_required_ebike = 0
        
        hourly_data.append([min_required_ebike, min_required_mechanical, total_salidas, salidas_electricas, salidas_mecanicas, 
                            total_entradas, entradas_electricas, entradas_mecanicas,
                            previous_hour, row['day_week'], row['day_month'], 
                            row['month'], satisfy_demand])
        
        # Reinicio de variables para la nueva hora
        hora_nueva = True
        disponibilidad_mecanicas_inicial = 0 # Valor inicial de bicicletas mecánicas a cada hora
        disponibilidad_electricas_inicial = 0 # Valor inicial de bicicletas eléctricas a cada hora
        primera_salida_mechanical = False
        primera_salida_ebike = False
        balance_mechanical = 0
        balance_ebike = 0
        disponibilidad_minima_mecanicas_tras_primera_salida = 100 # Número grande arbitrario
        disponibilidad_minima_electricas_tras_primera_salida = 100 # Número grande arbitrario

        salidas_mecanicas = 0
        salidas_electricas = 0
        entradas_mecanicas = 0
        entradas_electricas = 0
        no_bikes_counter = 0
        satisfy_demand = True
        previous_hour = row['hour']
    
    disponibilidad_mecanicas_anterior = disponibilidad_mecanicas_actual
    disponibilidad_electricas_anterior = disponibilidad_electricas_actual

# Convertir la lista acumulada a un DataFrame
columns = ['min_required_ebike', 'min_required_mechanical','total_salidas', 'salidas_electricas', 'salidas_mecanicas', 
           'total_entradas', 'entradas_electricas', 'entradas_mecanicas',
           'hour', 'day_week', 'day_month', 'month', 'satisfy_demand']
df_hourly = pd.DataFrame(hourly_data, columns=columns)

# Escribir el DataFrame resultante en un nuevo archivo llamado DataFramePerHour.csv
df_hourly.to_csv('DataFramePerHour.csv', index=False)