import subprocess

# Filtra todos los viajes relacionados con la estación 422 de 20221, 2022, y 2023 (hasta noviembre) y los agrupa en un sólo dataset.
# AVISO: Descomentar SÓLO cuando sea necesario, este es el script que filtra los datos de TODAS las estaciones, y puede llevar unos minutos.
# subprocess.run(['python3', 'scripts/first_filtering.py'])

subprocess.run(['python3', 'dataset_generation/scripts/1-Trips_422_filtering.py'])

subprocess.run(['python3', 'dataset_generation/scripts/2-Exits_and_Arrivals_422_classifier.py'])

subprocess.run(['python3', 'dataset_generation/scripts/3-Dataset_422_weather.py'])

subprocess.run(['python3', 'dataset_generation/scripts/4-Dataset_422_weather_cleaning.py'])

subprocess.run(['python3', 'dataset_generation/scripts/5-Dataset_422_weather_features.py'])

subprocess.run(['python3', 'dataset_generation/scripts/6-Dataset_422_weather_features_cleaning.py'])

subprocess.run(['python3', 'dataset_generation/scripts/7-Dataset_422_weather_features_scaling.py'])

subprocess.run(['python3', 'dataset_generation/scripts/8-Dataset_422_weather_features_scaling_cleaning.py'])
