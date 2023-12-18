import pandas as pd

# Cargar el dataset
file_path = 'Bicing_Trips_Total_2.csv'  # Reemplaza con la ruta de tu archivo
df = pd.read_csv(file_path)

# Inicializar el primer valor
initial_bikes = 11
df['available_bikes'] = initial_bikes

# Crear una columna temporal para indicar el cambio en el número de bicicletas
df['bike_change'] = df['trip_type'].map({'Llegada': 1, 'Salida': -1})

# Calcular la suma acumulativa de los cambios de bicicletas y sumarla al valor inicial
df['available_bikes'] = initial_bikes + df['bike_change'].cumsum()

# Eliminar la columna temporal
df.drop('bike_change', axis=1, inplace=True)

# Guardar el nuevo archivo CSV si es necesario
df.to_csv('Bicing_Trips_Total_3.csv', index=False)