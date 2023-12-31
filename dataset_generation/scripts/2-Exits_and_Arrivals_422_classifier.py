import pandas as pd

archivo_totales = 'dataset_generation/temporary_datasets/Trips_422.csv'

# Cargar datos originales
datos_totales = pd.read_csv(archivo_totales)

# Función para determinar el tipo de viaje
def determinar_tipo_viaje(fila):
    if fila['Start Station Id'] == 422:
        return 'Salida'
    elif fila['End Station Id'] == 422:
        return 'Llegada'
    else:
        return 'Otro'  # Por si acaso hay filas que no coinciden con 422

# Añadir la columna 'Trip Type'
datos_totales['trip_type'] = datos_totales.apply(determinar_tipo_viaje, axis=1)

# Eliminar las columnas 'Start Station Id' y 'End Station Id'
datos_totales = datos_totales.drop(columns=['Start Station Id', 'End Station Id'])

# Función para determinar el tiempo en función del tipo de viaje
def seleccionar_tiempo(fila):
    if fila['trip_type'] == 'Salida':
        return fila['Start Time']
    elif fila['trip_type'] == 'Llegada':
        return fila['End Time']
    else:
        return None  # Por si acaso hay filas que no son ni llegada ni salida

# Añadir la columna 'Time'
datos_totales['time'] = datos_totales.apply(seleccionar_tiempo, axis=1)

# Eliminar las columnas 'Start Time' y 'End Time'
datos_totales = datos_totales.drop(columns=['Start Time', 'End Time'])

# Guardar el nuevo archivo CSV si es necesario
datos_totales.to_csv('dataset_generation/temporary_datasets/Exits_and_Arrivals_422.csv', index=False)

# Mostrar las primeras filas del DataFrame modificado para verificar
print(datos_totales.head())