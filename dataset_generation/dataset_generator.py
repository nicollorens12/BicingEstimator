import subprocess
import os

# Filtra todos los viajes relacionados con la estación 422 de 20221, 2022, y 2023 (hasta noviembre) y los agrupa en un sólo dataset.
# AVISO: Descomentar SÓLO cuando sea necesario, este es el script que filtra los datos de TODAS las estaciones, y puede llevar unos minutos.
# subprocess.run(['python3', 'scripts/first_filtering.py'])

script_folder = 'dataset_generation/scripts'
scripts = [script for script in os.listdir(script_folder) if script.endswith('.py')]

# Ordenar los scripts en base a su nombre numérico
scripts.sort(key=lambda x: int(x.split('-')[0]))

for script in scripts:
    print(script)
    subprocess.run(['python3', os.path.join(script_folder, script)])
