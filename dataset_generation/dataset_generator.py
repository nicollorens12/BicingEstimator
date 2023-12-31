import subprocess

# Filtra todos los viajes relacionados con la estación 422 de 20221, 2022, y 2023 (hasta noviembre) y los agrupa en un sólo dataset.
# AVISO: Descomentar SÓLO cuando sea necesario, este es el script que filtra los datos de TODAS las estaciones, y puede llevar unos minutos.
# subprocess.run(['python3', 'scripts/first_filtering.py'])

# Clasifica los viajes por llegadas o salidas:
subprocess.run(['python3', 'scripts/second_filtering.py'])

# Crea un dataset que indica el número de llegadas y salidas en cada hora:
subprocess.run(['python3', 'scripts/grouping.py'])

# Crea un dataset por horas con la información meteorológica en las coordenadas de la estación:
subprocess.run(['python3', 'scripts/meteo_API_request.py'])

# Modifica el formato de fecha del dataset con la información meteorológica:
subprocess.run(['python3', 'scripts/converter_time.py'])

# Fusiona el dataset por horas con la información de llegadas y salidas con el dataset por horas con la información meteorológica:
subprocess.run(['python3', 'scripts/data_meteo_merge.py'])