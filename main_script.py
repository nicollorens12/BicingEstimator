import subprocess

# Ejecutar script1.py
subprocess.run(['python3', 'scripts/first_filtering.py'])

# Ejecutar script2.py
subprocess.run(['python3', 'scripts/second_filtering.py'])

# Ejecutar script3.py
subprocess.run(['python3', 'scripts/grouping.py'])

# Ejecutar script3.py
subprocess.run(['python3', 'scripts/data_meteo_merge.py'])