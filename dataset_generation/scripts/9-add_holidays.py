import pandas as pd
from datetime import datetime

# Cargar el dataset
data = pd.read_csv('dataset_generation/temporary_datasets/dataset_without_demand_satisfied.csv')

# Define los festivos de Barcelona para cada año
festivos = {
    '2021': ['2021-01-01', '2021-01-06', '2021-04-02', '2021-04-05', '2021-05-01', '2021-05-24', '2021-06-24', '2021-09-11', '2021-09-24', '2021-10-12', '2021-11-01', '2021-12-06', '2021-12-08', '2021-12-25'],
    '2022': ['2022-01-01', '2022-01-06', '2022-04-15', '2022-04-18', '2022-06-06', '2022-06-24', '2022-08-15', '2022-09-11', '2022-09-24', '2022-09-26', '2022-10-12', '2022-11-01', '2022-12-06', '2022-12-08', '2022-12-26'],
    '2023': ['2023-01-06', '2023-04-07', '2023-04-10', '2023-05-01', '2023-06-05', '2023-06-24', '2023-08-15', '2023-09-11', '2023-09-25', '2023-10-12', '2023-11-01', '2023-12-06', '2023-12-08', '2023-12-25', '2023-12-26']
}

# Define los periodos de clases y exámenes
periodos = {
    'clases': [
        ('2021-02-15', '2021-03-26'),
        ('2021-04-06', '2021-04-14'),
        ('2021-04-22', '2021-05-31'),
        ('2021-09-13', '2021-12-22'),
        ('2022-02-14', '2022-03-30'),
        ('2022-04-19', '2022-05-30'),
        ('2022-09-05', '2022-10-27'),
        ('2022-11-07', '2022-12-02'),
        ('2022-12-12', '2022-12-23'),
        ('2023-02-13', '2023-03-31'),
        ('2023-04-11', '2023-04-19'),
        ('2023-05-02', '2023-06-02'),
        ('2023-09-07', '2023-10-26'),
        ('2023-11-06', '2023-12-05'),
        ('2023-12-11', '2023-12-22')
    ],
    'examenes': [
        ('2021-01-07', '2021-01-22'),
        ('2021-04-15', '2021-04-21'),
        ('2021-06-01', '2021-06-22'),
        ('2022-01-10', '2022-01-21'),
        ('2022-03-31', '2022-04-06'),
        ('2022-05-31', '2022-06-22'),
        ('2022-10-28', '2022-11-04'),
        ('2023-01-09', '2023-01-20'),
        ('2023-04-20', '2023-04-26'),
        ('2023-06-06', '2023-06-23'),
        ('2023-10-27', '2023-11-03')
    ]
}

# Función para verificar si es día de trabajo
def es_dia_laboral(row):
    fecha = datetime(row['year'], row['month'], row['day'])
    fecha_str = fecha.strftime('%Y-%m-%d')
    if fecha.weekday() >= 5 or fecha_str in festivos[str(row['year'])]:
        return 0  # No es día laboral
    return 1  # Es día laboral

# Función para determinar el tipo de día de clase
def tipo_dia_clase(row):
    if row['working_day'] == 0:
        return 3  # No lectivo si no es un día laboral
    fecha = datetime(row['year'], row['month'], row['day'])
    for inicio, fin in periodos['clases']:
        if datetime.strptime(inicio, '%Y-%m-%d') <= fecha <= datetime.strptime(fin, '%Y-%m-%d'):
            return 1  # Lectivo
    for inicio, fin in periodos['examenes']:
        if datetime.strptime(inicio, '%Y-%m-%d') <= fecha <= datetime.strptime(fin, '%Y-%m-%d'):
            return 2  # Exámenes
    return 3  # No lectivo

# Aplica las funciones para crear las nuevas columnas
data['working_day'] = data.apply(es_dia_laboral, axis=1)
data['class_day'] = data.apply(tipo_dia_clase, axis=1)

# Guarda el nuevo dataset
data.to_csv('dataset_generation/temporary_datasets/dataset_without_demand_satisfied.csv', index=False)