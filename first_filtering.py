import pandas as pd
from datetime import datetime

# Nombres de los archivos CSV originales
archivo_2021 = 'Bicing_Trips_2021.csv'
archivo_2022 = 'Bicing_Trips_2022.csv'

# Cargar datos originales
datos_2021 = pd.read_csv(archivo_2021, delimiter=';')
datos_2022 = pd.read_csv(archivo_2022, delimiter=';')

# Array de estaciones a conservar
estaciones_a_conservar = [422]  # Puedes modificar esto con las estaciones que necesites

# Función para filtrar los datos por estaciones
def filtrar_por_estaciones(dataframe, estaciones):
    # Filtrar por estaciones de inicio y fin
    filtro = dataframe['Start Station Id'].isin(estaciones) | dataframe['End Station Id'].isin(estaciones)
    return dataframe[filtro]

# Eliminar la columna 'Trip Id' de ambos conjuntos de datos
datos_2021 = datos_2021.drop(columns=['Trip Id'])
datos_2022 = datos_2022.drop(columns=['Trip Id'])

# Limpiar valores no válidos o nulos en las columnas 'End Station Id'
datos_2021['End Station Id'] = pd.to_numeric(datos_2021['End Station Id'], errors='coerce')
datos_2022['End Station Id'] = pd.to_numeric(datos_2022['End Station Id'], errors='coerce')

# Reemplazar valores vacíos en 'End Station Id' por 1
datos_2021['End Station Id'] = datos_2021['End Station Id'].fillna(1).astype(int)
datos_2022['End Station Id'] = datos_2022['End Station Id'].fillna(1).astype(int)

# Convertir las columnas 'Start Station Id' y 'End Station Id' a enteros
datos_2021['Start Station Id'] = datos_2021['Start Station Id'].astype(int)
datos_2021['End Station Id'] = datos_2021['End Station Id'].astype(int)

datos_2022['Start Station Id'] = datos_2022['Start Station Id'].astype(int)
datos_2022['End Station Id'] = datos_2022['End Station Id'].astype(int)

# Filtrar por estaciones
datos_filtrados_2021 = filtrar_por_estaciones(datos_2021, estaciones_a_conservar)
datos_filtrados_2022 = filtrar_por_estaciones(datos_2022, estaciones_a_conservar)

# Filtrar por bicicletas eléctricas
datos_filtrados_2021 = datos_filtrados_2021[datos_filtrados_2021['Bike Model'] == 'ELECTRICA']
datos_filtrados_2022 = datos_filtrados_2022[datos_filtrados_2022['Bike Model'] == 'ELECTRICA']

# Eliminar la columna 'Bike Model'
datos_filtrados_2021 = datos_filtrados_2021.drop(columns=['Bike Model'])
datos_filtrados_2022 = datos_filtrados_2022.drop(columns=['Bike Model'])

# Concatenar ambos conjuntos de datos
datos_totales = pd.concat([datos_filtrados_2021, datos_filtrados_2022], ignore_index=True)

# Guardar el nuevo archivo CSV
datos_totales.to_csv('Bicing_Trips_Total_raw.csv', index=False)